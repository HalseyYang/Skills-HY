import * as cheerio from 'cheerio';
import { spawn } from 'node:child_process';
import { readFile, writeFile, readdir, realpath } from 'node:fs/promises';
import { resolve, sep } from 'node:path';

const hosts = new Set(['weixin.sogou.com', 'mp.weixin.qq.com']);
const challenge = /antispider|captcha|wappoc_appmsgcaptcha/i;
export class Failure extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

export function safeUrl(value, base = 'https://weixin.sogou.com') {
  const u = new URL(value, base);
  if (hosts.has(u.hostname) && challenge.test(u.pathname)) {
    throw new Failure('blocked', '站点要求验证，已停止请求。');
  }
  if (u.protocol !== 'https:' || !hosts.has(u.hostname) || u.port || u.username || u.password) {
    throw new Failure('error', '只接受搜狗微信或微信文章的公开 HTTPS 链接。');
  }
  for (const key of u.searchParams.keys()) {
    if (/^(key|pass_ticket|wap_sid2|uin)$/i.test(key)) {
      throw new Failure('error', '请使用不含临时授权参数的公开文章链接。');
    }
  }
  u.hash = '';
  return u;
}

export function articleUrl(value) {
  const u = safeUrl(value);
  return u.hostname === 'mp.weixin.qq.com' &&
    (/^\/s\/[^/]+$/.test(u.pathname) ||
     (u.pathname === '/s' && u.searchParams.has('__biz') && u.searchParams.has('mid')));
}

export function pageStatus(html, status = 200) {
  const $ = cheerio.load(html);
  if ([403, 429].includes(status) || $('#captcha, #seccodeImage, form[action*="antispider"]').length ||
      /请输入验证码|访问过于频繁|您的访问出错了|异常访问|环境异常/.test($('title').text()) ||
      /请输入验证码|访问过于频繁|您的访问出错了/.test($('body').clone().find('ul.news-list').remove().end().text())) {
    return 'blocked';
  }
  return status >= 400 ? 'error' : 'ok';
}

export async function requestPage(value, fetcher = fetch) {
  const url = safeUrl(value).href;
  const response = await fetcher(url, {
    redirect: 'manual', signal: AbortSignal.timeout(25000),
    headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' },
  });
  const chunks = []; let size = 0;
  for await (const chunk of response.body ?? []) {
    size += chunk.length;
    if (size > 2_000_000) throw new Failure('error', '页面超出 2MB 限制。');
    chunks.push(chunk);
  }
  const html = Buffer.concat(chunks).toString('utf8');
  const status = pageStatus(html, response.status);
  if (status !== 'ok') throw new Failure(status, `HTTP ${response.status}，页面不可正常读取。`);
  const location = response.headers.get('location');
  if (location) safeUrl(location, url);
  return { html, location, status: response.status, url };
}

// Search selectors follow the MIT upstream; only explicit epoch dates are trusted.
export function parseSearch(html, { days = 30, limit = 10, now = Date.now() } = {}) {
  const status = pageStatus(html);
  if (status !== 'ok') return { status, candidates: [], excluded: [], found: 0 };
  const $ = cheerio.load(html);
  if (!$('ul.news-list').length) {
    return { status: /没有找到|未找到|暂无结果/.test($('body').text()) ? 'no_results' : 'layout_changed', candidates: [], excluded: [], found: 0 };
  }
  const candidates = [], excluded = [], seen = new Set(); let found = 0;
  $('ul.news-list li').each((_, el) => {
    const item = $(el), link = item.find('h3 a').first();
    const title = link.text().trim(), href = link.attr('href');
    if (!title || !href) return;
    found++;
    const source = item.find('.s-p .all-time-y2, .s-p a.account').first().text().trim();
    const seconds = item.find('.s-p .s2 script').text().match(/\b(\d{10})\b/)?.[1];
    const time = seconds ? Number(seconds) * 1000 : NaN;
    const row = {
      id: found, title, source, summary: item.find('p.txt-info').text().trim(),
      published_at: Number.isFinite(time) ? new Date(time).toISOString() : null,
      date_text: item.find('.s-p .s2').clone().find('script').remove().end().text().trim(),
      evidence: 'search_snippet', url: null,
    };
    let reason;
    try { row.url = safeUrl(href).href; } catch { reason = 'unsupported_url'; }
    const key = `${source.normalize('NFKC')}|${title.normalize('NFKC').replace(/\s/g, '').toLowerCase()}`;
    if (!reason && (seen.has(key) || seen.has(row.url))) reason = 'duplicate';
    seen.add(key); seen.add(row.url);
    if (!reason && !Number.isFinite(time)) reason = 'unknown_date';
    if (!reason && time > now + 300_000) reason = 'future_date';
    if (!reason && time < now - days * 86400000) reason = 'older_than_window';
    if (!reason && candidates.length >= limit) reason = 'over_limit';
    if (reason) excluded.push({ ...row, reason }); else candidates.push(row);
  });
  return { status: candidates.length ? 'ok' : found ? 'filtered_empty' : 'layout_changed', found, candidates, excluded };
}

export function redirectFromHtml(html) {
  const $ = cheerio.load(html);
  const meta = $('meta[http-equiv]').filter((_, el) => $(el).attr('http-equiv').toLowerCase() === 'refresh').first().attr('content');
  if (meta?.match(/url\s*=\s*(.+)/i)) return meta.match(/url\s*=\s*(.+)/i)[1].replace(/^['"]|['"]$/g, '');
  const scripts = $('script').toArray().map(el => $(el).html()).join('\n');
  const direct = scripts.match(/(?:window\.)?location(?:\.href)?\s*=\s*(['"])(.*?)\1/);
  if (direct) return direct[2].replaceAll('&amp;', '&');
  // Decode literal URL fragments only, in source order; never evaluate page code.
  if (/location\.replace\(\s*url\s*\)/.test(scripts)) {
    const parts = [...scripts.matchAll(/\burl\s*\+=\s*(['"])(.*?)\1/g)].map(m => m[2]);
    if (parts.length) return parts.join('').replaceAll('&amp;', '&');
  }
  return null;
}

export async function resolveArticle(value, request = requestPage) {
  let url = safeUrl(value).href;
  for (let step = 0; step < 4; step++) {
    if (articleUrl(url)) return url;
    const page = await request(url);
    const target = page.location || redirectFromHtml(page.html);
    if (!target) throw new Failure('unresolved', '中转页没有可解析的公开文章链接。');
    url = safeUrl(target, url).href;
  }
  throw new Failure('unresolved', '跳转次数超出限制。');
}

export async function findArticles(dir) {
  const result = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) result.push(...await findArticles(path));
    else if (entry.isFile() && entry.name === 'article.json') result.push(path);
  }
  return result;
}

export async function verifyArticle(output, expectedUrl) {
  const paths = await findArticles(output);
  if (paths.length !== 1) throw new Failure('collection_failed', '未生成唯一的 article.json。');
  const metadata = JSON.parse(await readFile(paths[0], 'utf8'));
  if (metadata.source_url !== expectedUrl) throw new Failure('collection_failed', '正文来源与请求链接不一致。');
  const bodyPath = await realpath(resolve(paths[0], '../article.md'));
  const root = await realpath(output);
  if (!bodyPath.startsWith(root + sep)) throw new Failure('collection_failed', '正文路径越过输出目录。');
  const body = await readFile(bodyPath, 'utf8');
  const text = cheerio.load(metadata.content_html || '').text().trim();
  if (!metadata.title || text.length < 100 || body.trim().length < 100) {
    throw new Failure('collection_failed', '正文为空或过短，需人工核查。');
  }
  return { status: 'body_saved', title: metadata.title, author: metadata.author,
    published_at: metadata.publish_time, body_path: bodyPath, body_chars: text.length,
    metadata_path: paths[0], evidence: 'downloaded_article_unreviewed' };
}

export function parseArticle(html, url) {
  const status = pageStatus(html);
  if (status !== 'ok') throw new Failure(status, '文章页面要求验证，已停止。');
  const $ = cheerio.load(html);
  const title = $('#activity-name').text().trim() || $('meta[property="og:title"]').attr('content')?.trim();
  const content = $('#js_content').first().clone();
  content.find('script, style, iframe').remove();
  if (!title || !content.length || content.text().trim().length < 100) {
    throw new Failure('collection_failed', '未找到完整文字正文；可能是删除、付费、验证或非文字文章。');
  }
  const author = $('#js_name').text().trim() || null;
  const publishTime = $('#publish_time').text().trim() || null;
  const contentHtml = content.html();
  // Preserve text order without fetching images or executing embedded content.
  content.find('br').replaceWith('\n');
  content.find('p, section, div, li, h1, h2, h3, h4, blockquote, tr').each((_, el) => {
    $(el).prepend('\n').append('\n');
  });
  const body = content.text().replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n')
    .replace(/\n[ \t]+/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  return { metadata: { title, author, publish_time: publishTime, source_url: url,
    content_html: contentHtml, media_downloaded: false },
    markdown: `# ${title}\n\n来源：${url}\n公众号：${author || '未识别'}\n发布时间：${publishTime || '未识别，需人工核对'}\n\n${body}\n` };
}

export async function collectPublicArticle(url, output, request = requestPage) {
  if (!articleUrl(url)) throw new Failure('error', '需要公开微信文章链接。');
  const page = await request(url);
  if (page.location) {
    safeUrl(page.location, url);
    throw new Failure('unresolved', '正文入口发生跳转，请在浏览器确认公开原文链接。');
  }
  const { metadata, markdown } = parseArticle(page.html, url);
  await writeFile(resolve(output, 'source.html'), page.html);
  await writeFile(resolve(output, 'article.json'), JSON.stringify(metadata, null, 2) + '\n');
  await writeFile(resolve(output, 'article.md'), markdown);
  return verifyArticle(output, url);
}

export async function collectArticle(url, output, collector) {
  await readFile(collector);
  // Kill the whole process group on timeout so the downloader cannot keep crawling.
  const child = spawn('python3', [collector, url, '--single', '--no-media', '--output', output], {
    detached: process.platform !== 'win32', stdio: ['ignore', 'pipe', 'pipe'],
  });
  let log = '', timedOut = false;
  for (const stream of [child.stdout, child.stderr]) stream.on('data', chunk => { log = (log + chunk).slice(-200000); });
  const code = await new Promise((done, reject) => {
    const timer = setTimeout(() => {
      timedOut = true;
      try { process.kill(process.platform === 'win32' ? child.pid : -child.pid, 'SIGKILL'); } catch { /* already exited */ }
    }, 90000);
    child.once('error', e => { clearTimeout(timer); reject(e); });
    child.once('close', code => { clearTimeout(timer); done(code); });
  });
  log = log.replace(/((?:key|pass_ticket|wap_sid2|uin)=)[^\s&"'<>]+/gi, '$1[REDACTED]');
  await writeFile(resolve(output, 'collector.log'), log);
  if (timedOut) throw new Failure('collection_failed', '单篇下载超过 90 秒，已停止进程。');
  if (/AUTH_REQUIRED|请输入验证码|访问过于频繁|环境异常/.test(log)) throw new Failure('blocked', '正文采集要求验证，停止请求。');
  if (code !== 0) throw new Failure('collection_failed', `下载器退出码 ${code}，请查看 collector.log。`);
  return verifyArticle(output, url);
}
