#!/usr/bin/env node
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { pathToFileURL } from 'node:url';
import { Failure, safeUrl, requestPage, parseSearch, resolveArticle, collectArticle, collectPublicArticle } from './core.mjs';

const help = `公众号选题调研 (Node 22+)
search <keyword> --output <new-directory> [--days 30] [--limit 10]
read <public-url> --output <new-directory> [--collector <wechat_collect.py>]

每次只搜索一页，最多保留 10 条；read 每次只读一篇，不下载图片。
输出 result.json；遇验证立即停止。输出目录已存在时拒绝覆盖。`;

export function parseArgs(argv) {
  if (!argv.length || argv.includes('--help')) return { help: true };
  const [command, value, ...rest] = argv;
  if (!['search', 'read'].includes(command) || !value || value.startsWith('--')) throw new Error(help);
  const opts = { command, value, days: 30, limit: 10 };
  for (let i = 0; i < rest.length; i += 2) {
    const name = rest[i].replace(/^--/, '');
    if (!rest[i].startsWith('--') || !['output', ...(command === 'search' ? ['days', 'limit'] : ['collector'])].includes(name) || !rest[i + 1] || rest[i + 1].startsWith('--')) throw new Error('参数无效，使用 --help 查看用法。');
    opts[name] = rest[i + 1];
  }
  if (!opts.output) throw new Error('必须指定 --output 新目录。');
  for (const [name, max] of [['days', 365], ['limit', 10]]) {
    opts[name] = Number(opts[name]);
    if (!Number.isInteger(opts[name]) || opts[name] < 1 || opts[name] > max) throw new Error(`${name} 必须为 1–${max} 的整数。`);
  }
  if (!value.trim() || value.length > 2000) throw new Error('查询或链接为空或过长。');
  if (command === 'read') safeUrl(value);
  return opts;
}

export async function main(argv) {
  const opts = parseArgs(argv);
  if (opts.help) { console.log(help); return; }
  const output = resolve(opts.output);
  await mkdir(dirname(output), { recursive: true });
  await mkdir(output);
  const start = Date.now();
  const result = { command: opts.command, input: opts.value, started_at: new Date(start).toISOString() };
  try {
    if (opts.command === 'search') {
      const url = new URL('https://weixin.sogou.com/weixin');
      url.search = new URLSearchParams({ type: '2', query: opts.value, ie: 'utf8' }).toString();
      result.search_url = url.href; result.days = opts.days; result.limit = opts.limit;
      const page = await requestPage(url.href);
      if (page.location) throw new Failure('unresolved', '搜索入口跳转，未将跳转页当成结果。');
      await writeFile(resolve(output, 'search.html'), page.html);
      Object.assign(result, parseSearch(page.html, { ...opts, now: start }));
    } else {
      const url = await resolveArticle(opts.value);
      result.source_url = url;
      Object.assign(result, opts.collector
        ? await collectArticle(url, output, resolve(opts.collector))
        : await collectPublicArticle(url, output));
    }
  } catch (error) {
    result.status = error.status || 'error'; result.message = error.message;
  }
  result.elapsed_seconds = Number(((Date.now() - start) / 1000).toFixed(2));
  const path = resolve(output, 'result.json');
  await writeFile(path, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ ...result, result_path: path }, null, 2));
  if (!['ok', 'no_results', 'filtered_empty', 'body_saved'].includes(result.status)) process.exitCode = 2;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).catch(error => { console.error(error.message); process.exitCode = 1; });
}
