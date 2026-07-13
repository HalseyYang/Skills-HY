/* serializer.js Node 测试 —— 验证核心保存逻辑
 * 运行: node test-serializer.js
 * 注意：id 分配是文档顺序（含 html/body 等容器），测试按"内容/标签"定位 id，不假设顺序
 */
const fs = require('fs');
const path = require('path');

global.window = undefined;
require(path.join(__dirname, '..', 'assets', 'serializer.js'));
const S = global.HCEditorSerializer;

let pass = 0, fail = 0;
function assert(name, cond, detail) {
  if (cond) { pass++; console.log('  ✓ ' + name); }
  else { fail++; console.log('  ✗ ' + name + (detail ? '  →  ' + detail : '')); }
}

// 工具：在 idMap 里找"开标签包含某 class 或某文本上下文"的 id
function findIdByClass(idMap, html, cls) {
  return Object.keys(idMap).find(function (id) {
    const m = idMap[id];
    return html.slice(m.sourceIndex, m.sourceIndex + m.sourceLength).includes('class="' + cls + '"');
  });
}
function findIdByTag(idMap, html, tag) {
  // 找最后一个该 tag 的 id（用于"第二个 p"等场景）
  const ids = Object.keys(idMap).filter(function (id) { return idMap[id].tag === tag; });
  return ids;
}

console.log('\n=== 测试1: 打 ID ===');
{
  const sample = '<!DOCTYPE html>\n<html><head><style>.a{color:red}</style></head>\n<body>\n  <h1>标题</h1>\n  <div class="card"><p>段落</p></div>\n  <script>var x=1;<\/script>\n</body></html>';
  const r = S.injectIds(sample);
  assert('h1 打了 hc-id', /<h1[^>]*data-hc-id=/.test(r.html));
  assert('div 打了 hc-id', /<div[^>]*data-hc-id=/.test(r.html));
  assert('p 打了 hc-id', /<p[^>]*data-hc-id=/.test(r.html));
  assert('script 内部无 hc-id', !/var x=1;[^<]*data-hc-id/.test(r.html));
  assert('style 内部无 hc-id', !/color:red[^<]*data-hc-id/.test(r.html));
  // 容器元素也会被打标（html/head/body），加上 h1/div/p 共 6 个
  assert('ID 总数=6 (html/head/body/h1/div/p)', Object.keys(r.idMap).length === 6, '实际: ' + Object.keys(r.idMap).length);
  assert('idMap 含 tag 信息', r.idMap['hc-0'] && r.idMap['hc-0'].tag === 'html');
}

console.log('\n=== 测试2: 未改动 round-trip（关键！）===');
{
  const sample = '<!DOCTYPE html>\n<html><body>\n  <h1>标题</h1>\n  <p>段落</p>\n</body></html>';
  const r = S.injectIds(sample);
  const patched = S.applyPatches(r.html, r.idMap, {});
  assert('无改动时字节级一致', patched === r.html);
}

console.log('\n=== 测试3: style patch（改字号）===');
{
  const sample = '<html><body><h1>标题</h1></body></html>';
  const r = S.injectIds(sample);
  const h1Id = findIdByTag(r.idMap, r.html, 'h1')[0];
  const patched = S.applyPatches(r.html, r.idMap, { [h1Id]: { type: 'style', value: 'font-size:5vw' } });
  assert('注入了 font-size:5vw', /font-size:5vw/.test(patched));
  assert('文字"标题"保留', /标题/.test(patched));
  assert('闭标签</h1>保留', /<\/h1>/.test(patched));
}

console.log('\n=== 测试4: style patch 在已有 style 上合并 ===');
{
  const sample = '<html><body><h1 style="color:red">标题</h1></body></html>';
  const r = S.injectIds(sample);
  const h1Id = findIdByTag(r.idMap, r.html, 'h1')[0];
  const patched = S.applyPatches(r.html, r.idMap, { [h1Id]: { type: 'style', value: 'font-size:5vw' } });
  assert('保留了原 color:red', /color:red/.test(patched));
  assert('新增了 font-size:5vw', /font-size:5vw/.test(patched));
}

console.log('\n=== 测试5: text patch（改文字）===');
{
  const sample = '<html><body><h1>旧标题</h1></body></html>';
  const r = S.injectIds(sample);
  const h1Id = findIdByTag(r.idMap, r.html, 'h1')[0];
  const patched = S.applyPatches(r.html, r.idMap, { [h1Id]: { type: 'text', value: '新标题' } });
  assert('含新文字"新标题"', /新标题/.test(patched));
  assert('不含旧文字"旧标题"', !/旧标题/.test(patched));
}

console.log('\n=== 测试6: remove（删除第二个 p）===');
{
  const sample = '<html><body><div><p>保留</p><p>删除</p></div></body></html>';
  const r = S.injectIds(sample);
  const pIds = findIdByTag(r.idMap, r.html, 'p');
  const secondP = pIds[1]; // 第二个 p
  const patched = S.applyPatches(r.html, r.idMap, { [secondP]: { type: 'remove' } });
  assert('删除后含"保留"', /保留/.test(patched));
  assert('删除后不含"删除"', !/删除/.test(patched));
}

console.log('\n=== 测试7: duplicate（复制元素）===');
{
  const sample = '<html><body><div class="card">卡片</div></body></html>';
  const r = S.injectIds(sample);
  const cardId = findIdByClass(r.idMap, r.html, 'card');
  const patched = S.applyPatches(r.html, r.idMap, { [cardId]: { type: 'duplicate' } });
  const cardCount = (patched.match(/<div[^>]*card[^>]*>/g) || []).length;
  assert('复制后有两个 .card', cardCount === 2, '实际: ' + cardCount);
}

console.log('\n=== 测试8: 多元素混合改动（从后往前替换正确性）===');
{
  const sample = '<html><body><h1>大标题</h1><p>段落</p></body></html>';
  const r = S.injectIds(sample);
  const h1Id = findIdByTag(r.idMap, r.html, 'h1')[0];
  const pId = findIdByTag(r.idMap, r.html, 'p')[0];
  const patched = S.applyPatches(r.html, r.idMap, {
    [h1Id]: { type: 'text', value: '新大标题' },
    [pId]: { type: 'style', value: 'color:blue' }
  });
  assert('h1 文字被替换为新大标题', /新大标题/.test(patched));
  assert('p 加了 color:blue', /<p[^>]*color:blue/.test(patched));
  assert('原"段落"保留', /段落/.test(patched));
  assert('原"大标题"已移除', !/>大标题</.test(patched));
}

console.log('\n=== 测试9: validate 校验 ===');
{
  const ok = S.validate('<html><script>1<\/script><style>.a{}</style></html>');
  assert('正常HTML校验通过', ok.ok === true);
  const bad = S.validate('<html><script>1');
  assert('损坏HTML校验失败', bad.ok === false);
}

console.log('\n=== 测试10: 真实 PPT 样本打标 ===');
{
  const ppt = fs.readFileSync(path.join(__dirname, 'fixtures/ppt-sample.html'), 'utf8');
  const r = S.injectIds(ppt);
  const idCount = Object.keys(r.idMap).length;
  assert('PPT 样本成功打标', idCount > 10, 'ID数: ' + idCount);
  assert('script 块未被破坏', /go\(0\);/.test(r.html));
  assert('style 块未被破坏', /\.stat-card\{/.test(r.html));
  assert('打标后整体结构完整', S.validate(r.html).ok);
  const rt = S.applyPatches(r.html, r.idMap, {});
  assert('PPT 样本无改动 round-trip 一致', rt === r.html);
}

console.log('\n=== 测试11: 真实 PPT 样本改一处 style ===');
{
  const ppt = fs.readFileSync(path.join(__dirname, 'fixtures/ppt-sample.html'), 'utf8');
  const r = S.injectIds(ppt);
  const heroId = findIdByClass(r.idMap, r.html, 'h-hero');
  assert('找到 h-hero 元素', !!heroId);
  if (heroId) {
    const patched = S.applyPatches(r.html, r.idMap, {
      [heroId]: { type: 'style', value: 'margin-top:-5.56vh' }
    });
    assert('h-hero 注入了 margin-top:-5.56vh', /margin-top:-5.56vh/.test(patched));
    assert('改动后 script/style 仍完整', S.validate(patched).ok);
    assert('改动后封面标题文字保留', /封面标题/.test(patched));
  }
}

console.log('\n=== 测试12: 连续多次 style 合并不丢失（DRY）===');
{
  const sample = '<html><body><h1>标题</h1></body></html>';
  const r = S.injectIds(sample);
  const h1Id = findIdByTag(r.idMap, r.html, 'h1')[0];
  // 模拟编辑器连续记录两次改动（合并到同一个 change.value）
  let merged = S.mergeStyle('', 'margin-top:-5vh');
  merged = S.mergeStyle(merged, 'font-size:5vw');
  merged = S.mergeStyle(merged, 'margin-top:-8vh'); // 覆盖第一次
  const patched = S.applyPatches(r.html, r.idMap, { [h1Id]: { type: 'style', value: merged } });
  assert('margin-top 被覆盖为 -8vh（不是 -5vh）', /margin-top:-8vh/.test(patched));
  assert('不含旧的 -5vh', !/margin-top:-5vh/.test(patched));
  assert('font-size:5vw 保留', /font-size:5vw/.test(patched));
}

console.log('\n' + (fail === 0 ? '🎉 全部通过' : '⚠️ ' + fail + ' 项失败') + ' (通过 ' + pass + '/' + (pass + fail) + ')');
process.exit(fail === 0 ? 0 : 1);
