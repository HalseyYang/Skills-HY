# Skill: 自动上传输出文件到知识库

> 所有 WorkBuddy 生成的输出文件（PDF、Word、Excel、Markdown、图片等），自动上传到 **「个人知识库 > Workbuddy 审核」**。
>
> **目标知识库**：`i6YyWgwwoeNGXqrtspeovyL6QKXfhJWHaAqySYqbbY4=`（个人知识库）
> **目标文件夹**：`folder_7449993065539763`（Workbuddy 审核）
>
> **前置依赖**：腾讯ima skill（knowledge-base 模块）

## 使用时机

当任务完成并生成了可交付的文件（PDF、Word、Excel、Markdown、图片等）时，**自动执行**上传流程，无需用户额外提示。

## 上传流程（每生成一个文件执行一次）

### Step 1 — 前置检查（类型 + 大小）

```bash
SKILL_DIR="$HOME/.workbuddy/skills/腾讯ima"
KB_ID="i6YyWgwwoeNGXqrtspeovyL6QKXfhJWHaAqySYqbbY4="
FOLDER_ID="folder_7449993065539763"
IMA_CLIENT_ID="${IMA_OPENAPI_CLIENTID:-$(cat ~/.config/ima/client_id 2>/dev/null)}"
IMA_API_KEY="${IMA_OPENAPI_APIKEY:-$(cat ~/.config/ima/api_key 2>/dev/null)}"

ima_api() {
  local path="$1" body="$2"
  curl -s -X POST "https://ima.qq.com/$path" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "$body"
}

# 前置检查（类型 + 大小）
PREFLIGHT=$(node "$SKILL_DIR/knowledge-base/scripts/preflight-check.cjs" --file "$OUTPUT_FILE")
echo "$PREFLIGHT"
# 若 pass=false，直接终止，不上传
```

### Step 2 — 提取字段

```bash
FILE_NAME=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.file_name)")
FILE_EXT=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.file_ext)")
FILE_SIZE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.file_size))")
MEDIA_TYPE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.media_type))")
CONTENT_TYPE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.content_type)")
```

### Step 3 — 重名检查

```bash
ima_api "openapi/wiki/v1/check_repeated_names" "{
  \"params\": [{\"name\": \"$FILE_NAME\", \"media_type\": $MEDIA_TYPE}],
  \"knowledge_base_id\": \"$KB_ID\",
  \"folder_id\": \"$FOLDER_ID\"
}"
# 若 is_repeated=true，在文件名后追加 _YYYYMMDDHHmmss 后重试
```

### Step 4 — create_media

```bash
RESULT=$(ima_api "openapi/wiki/v1/create_media" "{
  \"file_name\": \"$FILE_NAME\",
  \"file_size\": $FILE_SIZE,
  \"content_type\": \"$CONTENT_TYPE\",
  \"knowledge_base_id\": \"$KB_ID\",
  \"file_ext\": \"$FILE_EXT\"
}")
MEDIA_ID=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.media_id)")
COS_SECRET_ID=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.secret_id)")
COS_SECRET_KEY=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.secret_key)")
COS_TOKEN=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.token)")
COS_BUCKET=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.bucket_name)")
COS_REGION=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.region)")
COS_KEY=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.data.cos_credential.cos_key)")
COS_START=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.data.cos_credential.start_time))")
COS_EXPIRE=$(echo "$RESULT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.data.cos_credential.expired_time))")
```

### Step 5 — COS 上传

```bash
node "$SKILL_DIR/knowledge-base/scripts/cos-upload.cjs" \
  --file "$OUTPUT_FILE" \
  --secret-id "$COS_SECRET_ID" \
  --secret-key "$COS_SECRET_KEY" \
  --token "$COS_TOKEN" \
  --bucket "$COS_BUCKET" \
  --region "$COS_REGION" \
  --cos-key "$COS_KEY" \
  --content-type "$CONTENT_TYPE" \
  --start-time "$COS_START" \
  --expired-time "$COS_EXPIRE"
```

### Step 6 — add_knowledge

```bash
ima_api "openapi/wiki/v1/add_knowledge" "{
  \"media_type\": $MEDIA_TYPE,
  \"media_id\": \"$MEDIA_ID\",
  \"title\": \"$FILE_NAME\",
  \"knowledge_base_id\": \"$KB_ID\",
  \"folder_id\": \"$FOLDER_ID\",
  \"file_info\": {
    \"cos_key\": \"$COS_KEY\",
    \"file_size\": $FILE_SIZE,
    \"file_name\": \"$FILE_NAME\"
  }
}"
```

## 批量处理

当一次性生成多个文件时：
1. 对所有文件**并行**执行 Step 1（前置检查）
2. 对通过的文件**串行**执行 Step 3（重名检查）
3. 对无冲突的文件**并行**执行 Step 4–6

## 错误处理

- 前置检查失败（类型不支持 / 大小超限）：**直接告知用户原因，不上传**
- COS 上传失败：终止，不调用 add_knowledge
- add_knowledge 失败：直接展示 `errmsg` 给用户

## 注意事项

- 文件上传**保持原始内容不变**，不得转码
- `folder_id` 使用 `folder_7449993065539763`，不要省略
- `file_name` 和 `title` 传同一个值（文件的原始完整文件名）
- 每次上传前确认凭证可用
