/* serializer.js —— 增量 patch 保存器
 * 借鉴 htmlcanvas-editor 的 serializer.js + domModel.js
 *
 * 三大职责：
 *   1. injectIds: 给原始 HTML 的元素打 data-hc-id 标记（正则遍历，不用 DOMParser 避免重排）
 *   2. applyPatches: 只替换被改动的元素，从后往前替换避免索引错位
 *   3. validate: 保存前结构完整性校验
 *
 * 关键原则：从不重新序列化整个文档，原文件的缩进/注释/script/style 一字不动。
 */
(function (global) {
  'use strict';

  // 要跳过的区域：script/style/注释/doctype —— patch 时绝不触碰
  function findSkipRegions(html) {
    const regions = [];
    const skipRegex = /(<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<!--[\s\S]*?-->|<!DOCTYPE[^>]*>)/gi;
    let m;
    while ((m = skipRegex.exec(html)) !== null) {
      regions.push([m.index, m.index + m[0].length]);
    }
    return regions;
  }
  function inAnyRegion(i, regions) {
    for (let k = 0; k < regions.length; k++) {
      if (i >= regions[k][0] && i < regions[k][1]) return true;
    }
    return false;
  }

  // 1. 打 ID：返回 { html, idMap }
  //    idMap: { 'hc-0': { sourceIndex, sourceLength, tag } }
  //    sourceIndex 是【打标后】的 HTML 里的字符位置（因为打标会改变后续索引）
  //    实现：用状态机遍历，遇到 script/style/注释 跳过到对应闭合标记
  //    （弃用 findSkipRegions 全局正则预扫——在浏览器引擎下对含 GLSL 的 HTML 边界算错）
  function injectIds(html) {
    const idMap = {};
    let counter = 0;
    const VOID = { area:1, base:1, br:1, col:1, embed:1, hr:1, img:1, input:1, link:1, meta:1, param:1, source:1, track:1, wbr:1 };

    const pieces = [];
    let lastIdx = 0;
    let i = 0;
    const len = html.length;

    while (i < len) {
      // 找下一个 '<'
      const lt = html.indexOf('<', i);
      if (lt < 0) break;

      // 判断这一段是不是要跳过的块（script/style/注释/doctype）
      const rest = html.slice(lt);
      let skipEnd = -1;

      if (/^<script\b/i.test(rest)) {
        skipEnd = findBlockEnd(html, lt, '</script', '>');
      } else if (/^<style\b/i.test(rest)) {
        skipEnd = findBlockEnd(html, lt, '</style', '>');
      } else if (rest.startsWith('<!--')) {
        skipEnd = html.indexOf('-->', lt + 4);
        if (skipEnd >= 0) skipEnd += 3;
      } else if (/^<!doctype/i.test(rest)) {
        skipEnd = html.indexOf('>', lt);
        if (skipEnd >= 0) skipEnd += 1;
      }

      if (skipEnd > lt) {
        // 整块跳过，原样进 pieces
        i = skipEnd;
        continue;
      }

      // 普通标签：用正则匹配开标签
      const tagMatch = /^<([a-zA-Z][a-zA-Z0-9]*)(\s[^<>]*)?\/?>/.exec(rest);
      if (!tagMatch) {
        i = lt + 1;
        continue;
      }

      const tagStart = lt;
      const fullMatch = tagMatch[0];
      const tagEnd = tagStart + fullMatch.length;
      const tag = tagMatch[1].toLowerCase();

      // 把 [lastIdx, tagStart) 的原文推进去
      pieces.push(html.slice(lastIdx, tagStart));

      if (/data-hc-id\s*=/.test(fullMatch)) {
        pieces.push(fullMatch);
      } else {
        const id = 'hc-' + (counter++);
        const isSelfClose = fullMatch.endsWith('/>');
        const insertAt = fullMatch.length - (isSelfClose ? 2 : 1);
        const newTag = fullMatch.slice(0, insertAt) + ' data-hc-id="' + id + '"' + fullMatch.slice(insertAt);
        pieces.push(newTag);
        idMap[id] = {
          sourceIndex: pieces.reduce((s, p) => s + p.length, 0) - newTag.length,
          sourceLength: newTag.length,
          tag: tag,
          isVoid: !!VOID[tag]
        };
      }
      lastIdx = tagEnd;
      i = tagEnd;
    }
    pieces.push(html.slice(lastIdx));
    return { html: pieces.join(''), idMap: idMap };
  }

  // 找块的闭合位置：从 start 开始找 closeTag（如 '</script'），返回 closeTag + '>' 之后的位置
  function findBlockEnd(html, start, closeTag, endChar) {
    const ci = html.toLowerCase().indexOf(closeTag, start);
    if (ci < 0) return start + 1;
    const ei = html.indexOf(endChar, ci);
    if (ei < 0) return start + 1;
    return ei + 1;
  }

  // 用栈匹配找配对闭标签 </tag> 的起始位置（从 startIndex 之后开始）
  function findCloseTagByStack(html, startIndex, tag) {
    const regex = new RegExp('<\\/?' + tag + '\\b[^>]*>', 'g');
    regex.lastIndex = startIndex;
    let depth = 0;
    let m;
    while ((m = regex.exec(html)) !== null) {
      const isClose = m[0].startsWith('</');
      const isSelfClose = m[0].endsWith('/>');
      if (isClose) {
        depth--;
        if (depth === 0) return m.index;
      } else if (!isSelfClose) {
        depth++;
      }
    }
    return -1;
  }

  // 合并 style 字符串：旧值 + 新属性覆盖
  function mergeStyle(oldVal, newProps) {
    const map = {};
    if (oldVal) {
      oldVal.split(';').filter(function (s) { return s.trim(); }).forEach(function (s) {
        const kv = s.split(':').map(function (x) { return x.trim(); });
        if (kv[0]) map[kv[0]] = kv[1];
      });
    }
    if (newProps) {
      newProps.split(';').filter(function (s) { return s.trim(); }).forEach(function (s) {
        const kv = s.split(':').map(function (x) { return x.trim(); });
        if (kv[0]) map[kv[0]] = kv[1];
      });
    }
    return Object.keys(map).map(function (k) { return k + ':' + map[k]; }).join(';');
  }

  // 2. 应用增量改动：返回 patch 后的完整 HTML
  //    changes: { 'hc-3': { type:'style', value:'margin-top:-5.56vh' }, ... }
  //    type 支持: 'style' | 'text' | 'remove' | 'duplicate'
  function applyPatches(html, idMap, changes) {
    let result = html;
    // 按 sourceIndex 从大到小（从后往前替换，避免索引错位）
    const sortedIds = Object.keys(changes)
      .filter(function (id) { return idMap[id]; })
      .sort(function (a, b) { return idMap[b].sourceIndex - idMap[a].sourceIndex; });

    for (let i = 0; i < sortedIds.length; i++) {
      const id = sortedIds[i];
      const meta = idMap[id];
      const change = changes[id];
      const before = result.slice(0, meta.sourceIndex);
      const tagRegion = result.slice(meta.sourceIndex, meta.sourceIndex + meta.sourceLength);
      const after = result.slice(meta.sourceIndex + meta.sourceLength);

      if (change.type === 'style') {
        let newTag;
        if (/style\s*=\s*"/.test(tagRegion)) {
          newTag = tagRegion.replace(/style\s*=\s*"([^"]*)"/, function (_full, val) {
            return 'style="' + mergeStyle(val, change.value) + '"';
          });
        } else if (tagRegion.endsWith('/>')) {
          newTag = tagRegion.slice(0, -2) + ' style="' + change.value + '"/>';
        } else {
          newTag = tagRegion.slice(0, -1) + ' style="' + change.value + '">';
        }
        result = before + newTag + after;
      } else if (change.type === 'text') {
        if (meta.isVoid) continue; // void 元素没文字
        const closeIdx = findCloseTagByStack(result, meta.sourceIndex, meta.tag);
        if (closeIdx !== -1) {
          const openEnd = meta.sourceIndex + meta.sourceLength;
          result = result.slice(0, openEnd) + change.value + result.slice(closeIdx);
        }
      } else if (change.type === 'remove') {
        if (meta.isVoid) {
          result = before + after;
        } else {
          const closeIdx = findCloseTagByStack(result, meta.sourceIndex, meta.tag);
          if (closeIdx !== -1) {
            const closeEnd = result.indexOf('>', closeIdx) + 1;
            result = before + result.slice(closeEnd);
          }
        }
      } else if (change.type === 'duplicate') {
        if (meta.isVoid) {
          result = before + tagRegion + tagRegion + after;
        } else {
          const closeIdx = findCloseTagByStack(result, meta.sourceIndex, meta.tag);
          if (closeIdx !== -1) {
            const closeEnd = result.indexOf('>', closeIdx) + 1;
            const elementHtml = result.slice(meta.sourceIndex, closeEnd);
            result = result.slice(0, closeEnd) + elementHtml + result.slice(closeEnd);
          }
        }
      }
    }
    return result;
  }

  // 3. 保存前校验
  function validate(html) {
    const scriptOpen = (html.match(/<script\b/gi) || []).length;
    const scriptClose = (html.match(/<\/script>/gi) || []).length;
    const styleOpen = (html.match(/<style\b/gi) || []).length;
    const styleClose = (html.match(/<\/style>/gi) || []).length;
    if (scriptOpen !== scriptClose) return { ok: false, reason: 'script 块数量不匹配 (' + scriptOpen + ' vs ' + scriptClose + ')' };
    if (styleOpen !== styleClose) return { ok: false, reason: 'style 块数量不匹配 (' + styleOpen + ' vs ' + styleClose + ')' };
    if (/<hc-temp-marker/.test(html)) return { ok: false, reason: '残留临时标记' };
    return { ok: true };
  }

  global.HCEditorSerializer = { injectIds: injectIds, applyPatches: applyPatches, validate: validate, mergeStyle: mergeStyle, findCloseTagByStack: findCloseTagByStack };
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
