/* build-editable.js —— 构建脚本：把原始 HTML + 编辑器资源拼成"可编辑版"
 * 用法: node build-editable.js <原始HTML路径> <输出路径> [文件名]
 *
 * 这是 editable-html skill 工具箱的一部分。
 *
 * 存储方式：原始 PPT 用 base64 编码存在 data 属性里。
 *   - 100% 可靠：base64 不含任何 HTML 特殊字符（< > " ' 等），不会破坏外层结构
 *   - 原始内容不管是 GLSL 着色器、多个 script、特殊字符，都能完整还原
 *   - 读取时 atob 解码 + UTF-8 解码
 */
const fs = require('fs');
const path = require('path');

const SRC = process.argv[2];
const OUT = process.argv[3];
const FILENAME = process.argv[4] || 'edited';

if (!SRC || !OUT) {
  console.error('用法: node build-editable.js <原始HTML路径> <输出路径> [文件名]');
  process.exit(1);
}

// assets 目录相对于本脚本的位置（本仓库结构：build-editable.js 与 assets/ 同级）
const ASSETS = path.join(__dirname, 'assets');
const originalHtml = fs.readFileSync(SRC, 'utf8');
const editorCss = fs.readFileSync(path.join(ASSETS, 'editor.css'), 'utf8');
const serializerJs = fs.readFileSync(path.join(ASSETS, 'serializer.js'), 'utf8');
const editorJs = fs.readFileSync(path.join(ASSETS, 'editor.js'), 'utf8');

// base64 编码原始 PPT（UTF-8 → base64）
// 注意：btoa 不支持非 ASCII，要先 encodeURIComponent 处理
const b64 = Buffer.from(originalHtml, 'utf8').toString('base64');

const editableHtml =
'<!DOCTYPE html>\n' +
'<html lang="zh-CN">\n' +
'<head>\n' +
'<meta charset="UTF-8">\n' +
'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
'<title>' + FILENAME + ' (可编辑版)</title>\n' +
'<style>\n' + editorCss + '\n</style>\n' +
'</head>\n' +
'<body>\n' +
'<!-- 原始内容用 base64 存这里（避免任何特殊字符破坏结构） -->\n' +
'<div id="hce-source" data-source="' + b64 + '"></div>\n' +
'<!-- 编辑器代码（serializer 保存逻辑 + editor 主逻辑） -->\n' +
'<script>\n' + serializerJs + '\n</' + 'script>\n' +
'<script>\n' + editorJs + '\n</' + 'script>\n' +
'<!-- 启动：页面加载后自动进入编辑 -->\n' +
'<script>\n' +
'  document.addEventListener("DOMContentLoaded", function(){\n' +
'    HCEditor.autoEnter({filename: "' + FILENAME + '"});\n' +
'  });\n' +
'</' + 'script>\n' +
'</body>\n' +
'</html>\n';

fs.writeFileSync(OUT, editableHtml, 'utf8');
console.log('已生成可编辑版: ' + OUT);
console.log('  原始大小: ' + originalHtml.length + ' 字符');
console.log('  base64 大小: ' + b64.length + ' 字符');
console.log('  可编辑版大小: ' + editableHtml.length + ' 字符 (含编辑器代码)');
console.log('  文件名标识: ' + FILENAME);
