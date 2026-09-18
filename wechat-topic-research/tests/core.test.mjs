import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { safeUrl, articleUrl, pageStatus, parseSearch, redirectFromHtml, resolveArticle, requestPage, verifyArticle, collectArticle, parseArticle, collectPublicArticle } from '../scripts/core.mjs';
import { parseArgs, main } from '../scripts/research.mjs';

const now = Date.parse('2026-09-06T10:00:00+08:00');
const sampleUrl = 'https://mp.weixin.qq.com/s/test-article';
function row({ title = '测试教程', url = '/link?url=test', source = '测试号', time = now - 86400000 } = {}) {
  return `<li><h3><a href="${url}">${title}</a></h3><p class="txt-info">仅为搜索摘要</p><div class="s-p"><span class="all-time-y2">${source}</span><span class="s2">${time ? `<script>timeConvert('${time / 1000}')</script>` : '昨天'}</span></div></li>`;
}
const page = rows => `<ul class="news-list">${rows.join('')}</ul>`;

const articleFixture = `<h1 id="activity-name">正文测试</h1><a id="js_name">测试账号</a><span id="publish_time">2026-09-08</span><div id="js_content"><p>${'第一段文字。'.repeat(30)}</p><p>结尾文字<br>下一行</p><script>DO_NOT_RUN</script></div>`;

test('内置采集无需用户目录和 Python，保留正文段落和来源', async () => {
  assert.equal(parseArgs(['read', sampleUrl, '--output', '/tmp/example']).collector, undefined);
  const parsed = parseArticle(articleFixture, sampleUrl);
  assert.equal(parsed.metadata.author, '测试账号');
  assert.equal(parsed.metadata.publish_time, '2026-09-08');
  assert.match(parsed.markdown, /结尾文字\n下一行/);
  assert.doesNotMatch(parsed.markdown, /DO_NOT_RUN/);
  const dir = await mkdtemp(join(tmpdir(), 'wechat-native-'));
  try {
    let requests = 0;
    const result = await collectPublicArticle(sampleUrl, dir, async () => {
      requests++; return { html: articleFixture };
    });
    assert.equal(requests, 1);
    assert.equal(result.status, 'body_saved');
    assert.equal(result.title, '正文测试');
  } finally { await rm(dir, { recursive: true, force: true }); }
});

test('内置采集拒绝摘要、验证和未知正文，不编造日期', () => {
  assert.throws(() => parseArticle('<title>请输入验证码</title>', sampleUrl), { status: 'blocked' });
  assert.throws(() => parseArticle('<h1>文章</h1><p>仅摘要</p>', sampleUrl), { status: 'collection_failed' });
  assert.equal(parseArticle(articleFixture.replace('<span id="publish_time">2026-09-08</span>', ''), sampleUrl).metadata.publish_time, null);
});

test('内置采集遇挑战跳转停止，不追加请求', async () => {
  let requests = 0;
  await assert.rejects(collectPublicArticle(sampleUrl, '/unused', async () => {
    requests++; return { location: 'https://mp.weixin.qq.com/mp/wappoc_appmsgcaptcha', html: '' };
  }), { status: 'blocked' });
  assert.equal(requests, 1);
});

test('日期明确、摘要标签、时区统一', () => {
  const r = parseSearch(page([row()]), { now });
  assert.equal(r.status, 'ok');
  assert.equal(r.candidates[0].published_at, '2026-09-05T02:00:00.000Z');
  assert.equal(r.candidates[0].evidence, 'search_snippet');
  assert.equal(r.candidates[0].url, 'https://weixin.sogou.com/link?url=test');
});

test('排除旧文、时间未知、未来日期、重复标题与重复链接', () => {
  const r = parseSearch(page([
    row(), row({ url: '/link?url=other' }), row({ title: '另一个标题' }),
    row({ title: '旧', url: '/link?url=old', time: now - 400 * 86400000 }),
    row({ title: '未知', url: '/link?url=unknown', time: null }),
    row({ title: '未来', url: '/link?url=future', time: now + 86400000 }),
  ]), { now });
  assert.equal(r.candidates.length, 1);
  assert.deepEqual(r.excluded.map(x => x.reason), ['duplicate', 'duplicate', 'older_than_window', 'unknown_date', 'future_date']);
});

test('数量限制在过滤后应用，不由旧文章挤掉新条目', () => {
  const r = parseSearch(page([row({ time: now - 400 * 86400000 }), row({ title: '新', url: '/link?url=new' }), row({ title: '新二', url: '/link?url=new2' })]), { now, limit: 1 });
  assert.equal(r.candidates[0].title, '新');
  assert.equal(r.excluded[1].reason, 'over_limit');
});

test('验证、空结果、版式改变分开，不把文章标题当验证码', () => {
  assert.equal(pageStatus('<title>请输入验证码</title>'), 'blocked');
  assert.equal(pageStatus('<p>no</p>', 429), 'blocked');
  assert.equal(pageStatus(page([row({ title: '请输入验证码问题教程' })])), 'ok');
  assert.equal(parseSearch('<p>没有找到相关内容</p>').status, 'no_results');
  assert.equal(parseSearch('<div>unknown layout</div>').status, 'layout_changed');
  assert.equal(parseSearch(page([row({ time: now - 400 * 86400000 })]), { now }).status, 'filtered_empty');
});

test('仅允许精确域名和 HTTPS，拒绝授权链接与挑战路径', () => {
  for (const u of ['https://mp.weixin.qq.com.evil.test/s/x', 'http://mp.weixin.qq.com/s/x', 'https://localhost/s/x', 'https://weixin.sogou.com:8080', 'https://user@mp.weixin.qq.com/s/x', 'https://mp.weixin.qq.com/s/x?pass_ticket=secret']) assert.throws(() => safeUrl(u));
  assert.throws(() => safeUrl('http://weixin.sogou.com/antispider/?from=abc'), { status: 'blocked' });
  assert.equal(articleUrl(sampleUrl), true);
  assert.equal(articleUrl('https://mp.weixin.qq.com/'), false);
});

test('安全解析 meta、字面量跳转、单双引号混排；不执行脚本', () => {
  assert.equal(redirectFromHtml(`<meta content="0;url=${sampleUrl}" http-equiv="refresh">`), sampleUrl);
  assert.equal(redirectFromHtml(`<script>location.href='${sampleUrl}'</script>`), sampleUrl);
  assert.equal(redirectFromHtml(`<script>var url='';url+='https://mp.';url+="weixin.qq.com/s/";url+='test-article';location.replace(url);</script>`), sampleUrl);
  assert.equal(redirectFromHtml('<script>location.href=eval(secret)</script>'), null);
});

test('中转验证立即停止，不访问挑战页面或下一个链接', async () => {
  let calls = 0;
  await assert.rejects(resolveArticle('https://weixin.sogou.com/link?url=x', async () => {
    calls++; return { location: 'http://weixin.sogou.com/antispider/', html: '' };
  }), { status: 'blocked' });
  assert.equal(calls, 1);
});

test('跳转最多四次；微信原文直接交给采集器', async () => {
  let calls = 0;
  assert.equal(await resolveArticle(sampleUrl, async () => { calls++; }), sampleUrl);
  assert.equal(calls, 0);
  await assert.rejects(resolveArticle('https://weixin.sogou.com/link?url=x', async () => { calls++; return { location: '/link?url=loop', html: '' }; }), { status: 'unresolved' });
  assert.equal(calls, 4);
});

test('HTTP 403 被当作 blocked，失败时不自动重试', async () => {
  let calls = 0;
  await assert.rejects(requestPage('https://weixin.sogou.com/weixin', async () => { calls++; return new Response('denied', { status: 403 }); }), { status: 'blocked' });
  assert.equal(calls, 1);
});

test('拒绝无效参数、过量请求和 read 日期参数', () => {
  for (const args of [['search', 'AI'], ['search', 'AI', '--output', '/tmp/x', '--limit', '50'], ['search', 'AI', '--output', '/tmp/x', '--days', '-1'], ['read', sampleUrl, '--output', '/tmp/x', '--days', '30']]) assert.throws(() => parseArgs(args));
  assert.equal(parseArgs(['search', 'AI', '--output', '/tmp/x']).limit, 10);
});

test('拒绝复用输出目录，避免旧文件冒充新采集', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'wechat-test-'));
  try { await assert.rejects(main(['search', 'AI', '--output', dir]), { code: 'EEXIST' }); }
  finally { await rm(dir, { recursive: true, force: true }); }
});

test('正文验证：缺来源、空正文、错 URL 都不算成功', async () => {
  const dir = await mkdtemp(join(tmpdir(), 'wechat-test-'));
  try {
    await assert.rejects(verifyArticle(dir, sampleUrl), { status: 'collection_failed' });
    const metadata = { title: '测试', source_url: sampleUrl, content_html: '<p>' + '正文'.repeat(100) + '</p>' };
    await writeFile(join(dir, 'article.json'), JSON.stringify(metadata));
    await writeFile(join(dir, 'article.md'), '正文'.repeat(100));
    assert.equal((await verifyArticle(dir, sampleUrl)).status, 'body_saved');
    await assert.rejects(verifyArticle(dir, sampleUrl + '-wrong'), { status: 'collection_failed' });
    await writeFile(join(dir, 'article.md'), '');
    await assert.rejects(verifyArticle(dir, sampleUrl), { status: 'collection_failed' });
  } finally { await rm(dir, { recursive: true, force: true }); }
});

test('可选 Python 采集器衔接使用独立目录和 no-media', { skip: spawnSync('python3', ['--version']).status !== 0 }, async () => {
  const dir = await mkdtemp(join(tmpdir(), 'wechat-test-'));
  try {
    const script = join(dir, 'fixture_collector.py');
    await writeFile(script, `import sys,json,pathlib\nassert '--single' in sys.argv and '--no-media' in sys.argv\no=pathlib.Path(sys.argv[sys.argv.index('--output')+1])\n(o/'article.json').write_text(json.dumps({'title':'fixture','source_url':sys.argv[1],'content_html':'text '*80}))\n(o/'article.md').write_text('text '*80)\nprint('fixture only')\n`);
    const output = join(dir, 'output'); await mkdir(output);
    const result = await collectArticle(sampleUrl, output, script);
    assert.equal(result.status, 'body_saved');
    assert.equal(result.body_chars, 399);
    assert.equal(result.evidence, 'downloaded_article_unreviewed');
  } finally { await rm(dir, { recursive: true, force: true }); }
});
