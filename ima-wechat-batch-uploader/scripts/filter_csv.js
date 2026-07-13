/**
 * filter_csv.js - 筛选 CSV 中的公众号文章，排除非法规类内容
 *
 * 用法: node filter_csv.js <csv_path> [exclude_keywords_file] [output_dir]
 *
 * 输入: CSV 文件（需包含 title 和 url 列）
 * 输出:
 *   - filtered_articles.json   保留的文章列表
 *   - excluded_articles.json   被排除的文章列表
 *   - upload_list.txt          纯文本预览
 */

const fs = require('fs');
const path = require('path');

// 默认排除关键词
const DEFAULT_EXCLUDE_KEYWORDS = [
  '招聘', '热招职位', '节日', '五一', '新春快乐', '抽奖', '问卷',
  '和BSI一起', 'BSI人', '医疗最新使命', '邀请函', '相约', 'CMEF',
  '展会', '倒计时', '收官', '圆满落幕', '同愿', '并肩', '携', '助力可持续发展',
  '报名表', '报名 |', '报名倒计时', '课程限时', '新课推荐', '最新课表', '经典课程', '培训报名',
  '最后席位', '开放报名', '紧急通知', '参会指南'
];

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node filter_csv.js <csv_path> [exclude_keywords_file] [output_dir]');
    process.exit(1);
  }
  return {
    csvPath: args[0],
    keywordsFile: args[1] || null,
    outputDir: args[2] || '.'
  };
}

function loadExcludeKeywords(keywordsFile) {
  if (keywordsFile && fs.existsSync(keywordsFile)) {
    const content = fs.readFileSync(keywordsFile, 'utf8');
    return content.split('\n').map(l => l.trim()).filter(l => l.length > 0);
  }
  return DEFAULT_EXCLUDE_KEYWORDS;
}

function parseCSV(csvPath) {
  const content = fs.readFileSync(csvPath, 'utf8');
  // Handle BOM
  const cleanContent = content.replace(/^\uFEFF/, '');
  const lines = cleanContent.split('\n').filter(l => l.trim().length > 0);
  if (lines.length < 2) return [];

  // Parse header
  const headers = parseCSVLine(lines[0]);
  const titleIdx = headers.findIndex(h => h.toLowerCase() === 'title');
  const urlIdx = headers.findIndex(h => h.toLowerCase() === 'url');

  if (titleIdx === -1 || urlIdx === -1) {
    throw new Error('CSV must contain "title" and "url" columns');
  }

  const records = [];
  for (let i = 1; i < lines.length; i++) {
    const cols = parseCSVLine(lines[i]);
    const title = (cols[titleIdx] || '').trim();
    const url = (cols[urlIdx] || '').trim();
    if (title && url) {
      records.push({ title, url });
    }
  }
  return records;
}

function parseCSVLine(line) {
  const cols = [];
  let current = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      cols.push(current.trim());
      current = '';
    } else {
      current += c;
    }
  }
  cols.push(current.trim());
  return cols;
}

function main() {
  const { csvPath, keywordsFile, outputDir } = parseArgs();

  if (!fs.existsSync(csvPath)) {
    console.error(`Error: CSV file not found: ${csvPath}`);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const excludeKeywords = loadExcludeKeywords(keywordsFile);
  const articles = parseCSV(csvPath);

  const seen = new Set();
  const kept = [];
  const excluded = [];

  for (const article of articles) {
    // Deduplicate by title
    if (seen.has(article.title)) {
      excluded.push({ title: article.title, reason: '重复' });
      continue;
    }
    seen.add(article.title);

    // Check exclusion keywords
    let reason = null;
    for (const kw of excludeKeywords) {
      if (article.title.includes(kw)) {
        reason = `包含关键词「${kw}」`;
        break;
      }
    }

    if (reason) {
      excluded.push({ title: article.title, reason });
    } else {
      kept.push({ title: article.title, url: article.url });
    }
  }

  // Write outputs
  fs.writeFileSync(
    path.join(outputDir, 'filtered_articles.json'),
    JSON.stringify({ kept, total: articles.length, kept_count: kept.length, excluded_count: excluded.length }, null, 2)
  );

  fs.writeFileSync(
    path.join(outputDir, 'excluded_articles.json'),
    JSON.stringify({ excluded, total: articles.length, excluded_count: excluded.length }, null, 2)
  );

  const uploadList = kept.map((a, i) => `${i + 1}. ${a.title}\n   ${a.url}`).join('\n\n');
  fs.writeFileSync(path.join(outputDir, 'upload_list.txt'), uploadList);

  console.log(`=== 筛选结果 ===`);
  console.log(`总计: ${articles.length} 篇`);
  console.log(`保留: ${kept.length} 篇`);
  console.log(`排除: ${excluded.length} 篇`);
  console.log(`\n输出文件:`);
  console.log(`  - ${path.join(outputDir, 'filtered_articles.json')}`);
  console.log(`  - ${path.join(outputDir, 'excluded_articles.json')}`);
  console.log(`  - ${path.join(outputDir, 'upload_list.txt')}`);
}

main();
