/**
 * batch_upload.js - 批量上传公众号文章到 IMA 知识库
 *
 * 用法: node batch_upload.js <articles_json> <kb_id> <folder_id> [batch_size]
 *
 * 参数:
 *   articles_json  - filter_csv.js 生成的 filtered_articles.json 路径
 *   kb_id          - API 知识库 ID (如 VUJ-nc8nXeEQWHi9xrAIvk8VYmN8Lp39W1JCM777NQ4=)
 *   folder_id      - 目标文件夹 ID (如 folder_7476093149796694)
 *   batch_size     - 每批数量，默认 10 (最大 10)
 *
 * 环境要求:
 *   IMA_OPENAPI_CLIENTID 和 IMA_OPENAPI_APIKEY 环境变量已设置
 */

const fs = require('fs');
const https = require('https');

const IMA_HOST = 'ima.qq.com';
const IMA_API_BASE = '/openapi/wiki/v1';

function getCredentials() {
  // 优先从环境变量读取
  if (process.env.IMA_OPENAPI_CLIENTID && process.env.IMA_OPENAPI_APIKEY) {
    return {
      clientId: process.env.IMA_OPENAPI_CLIENTID.trim(),
      apiKey: process.env.IMA_OPENAPI_APIKEY.trim()
    };
  }

  // 从配置文件读取（支持 UTF-8 和 UTF-16 LE 编码）
  const clientIdPath = `${process.env.USERPROFILE}/.config/ima/client_id`;
  const apiKeyPath = `${process.env.USERPROFILE}/.config/ima/api_key`;

  let clientId, apiKey;

  try {
    const cidBuf = fs.readFileSync(clientIdPath);
    // 检测 BOM 判断编码
    if (cidBuf.length >= 2 && cidBuf[0] === 0xFF && cidBuf[1] === 0xFE) {
      clientId = cidBuf.toString('utf16le').replace(/^\uFEFF/, '').trim();
    } else {
      clientId = cidBuf.toString('utf8').replace(/^\uFEFF/, '').trim();
    }
  } catch (e) {
    throw new Error(`无法读取 client_id: ${e.message}`);
  }

  try {
    const akBuf = fs.readFileSync(apiKeyPath);
    if (akBuf.length >= 2 && akBuf[0] === 0xFF && akBuf[1] === 0xFE) {
      apiKey = akBuf.toString('utf16le').replace(/^\uFEFF/, '').trim();
    } else {
      apiKey = akBuf.toString('utf8').replace(/^\uFEFF/, '').trim();
    }
  } catch (e) {
    throw new Error(`无法读取 api_key: ${e.message}`);
  }

  return { clientId, apiKey };
}

function apiCall(endpoint, body) {
  return new Promise((resolve, reject) => {
    const { clientId, apiKey } = getCredentials();
    const payload = JSON.stringify(body);
    const req = https.request({
      hostname: IMA_HOST,
      port: 443,
      path: `${IMA_API_BASE}${endpoint}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'ima-openapi-clientid': clientId,
        'ima-openapi-apikey': apiKey,
        'ima-openapi-ctx': 'skill_version=1.1.7'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data, status: res.statusCode });
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: node batch_upload.js <articles_json> <kb_id> <folder_id> [batch_size]');
    process.exit(1);
  }
  return {
    articlesJson: args[0],
    kbId: args[1],
    folderId: args[2],
    batchSize: Math.min(parseInt(args[3]) || 10, 10)
  };
}

async function main() {
  const { articlesJson, kbId, folderId, batchSize } = parseArgs();

  if (!fs.existsSync(articlesJson)) {
    console.error(`Error: Articles JSON not found: ${articlesJson}`);
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(articlesJson, 'utf8'));
  const articles = data.kept || data;

  // Clean URLs: replace &amp; with &
  const cleanedArticles = articles.map(a => ({
    ...a,
    url: a.url.replace(/&amp;/g, '&')
  }));

  console.log(`=== 批量上传 ===`);
  console.log(`知识库: ${kbId}`);
  console.log(`文件夹: ${folderId}`);
  console.log(`文章总数: ${cleanedArticles.length}`);
  console.log(`每批数量: ${batchSize}`);
  console.log(`预计批次: ${Math.ceil(cleanedArticles.length / batchSize)}`);
  console.log();

  const totalBatches = Math.ceil(cleanedArticles.length / batchSize);
  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < totalBatches; i++) {
    const batch = cleanedArticles.slice(i * batchSize, (i + 1) * batchSize);
    const urls = batch.map(a => a.url);

    console.log(`\n[批次 ${i + 1}/${totalBatches}] 上传 ${urls.length} 篇...`);

    try {
      const result = await apiCall('/import_urls', {
        knowledge_base_id: kbId,
        folder_id: folderId,
        urls: urls
      });

      if (result.code === 0 || result.ret_code === 0) {
        console.log(`  成功: ${urls.length} 篇`);
        successCount += urls.length;
      } else {
        console.log(`  失败: ${result.message || result.msg || JSON.stringify(result)}`);
        failCount += urls.length;
      }
    } catch (err) {
      console.log(`  错误: ${err.message}`);
      failCount += urls.length;
    }

    // Wait between batches
    if (i < totalBatches - 1) {
      console.log(`  等待 2 秒...`);
      await sleep(2000);
    }
  }

  console.log(`\n=== 上传完成 ===`);
  console.log(`成功: ${successCount} 篇`);
  console.log(`失败: ${failCount} 篇`);
  console.log(`总计: ${cleanedArticles.length} 篇`);

  // Verify
  console.log(`\n等待 5 秒后验证...`);
  await sleep(5000);

  let allArticles = [];
  let cursor = '';
  let page = 0;
  while (page < 10) {
    const result = await apiCall('/get_knowledge_list', {
      knowledge_base_id: kbId,
      folder_id: folderId,
      limit: 50,
      cursor: cursor
    });
    if (result.code !== 0) break;
    allArticles = allArticles.concat(result.data.knowledge_list);
    if (result.data.is_end) break;
    cursor = result.data.next_cursor;
    page++;
  }

  const goodArticles = allArticles.filter(a => !a.title.startsWith('http'));
  const badArticles = allArticles.filter(a => a.title.startsWith('http'));

  console.log(`\n验证结果:`);
  console.log(`  文件夹文章总数: ${allArticles.length}`);
  console.log(`  标题正确: ${goodArticles.length} 篇`);
  console.log(`  标题为 URL (需删除): ${badArticles.length} 篇`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
