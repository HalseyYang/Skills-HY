import json
import os
import urllib.request
import urllib.parse

# Load credentials
client_id = os.environ.get("IMA_OPENAPI_CLIENTID") or ""
api_key = os.environ.get("IMA_OPENAPI_APIKEY") or ""

if not client_id or not api_key:
    # Try reading from config files
    config_dir = os.path.expanduser("~/.config/ima/")
    client_id_file = os.path.join(config_dir, "client_id")
    api_key_file = os.path.join(config_dir, "api_key")
    if os.path.exists(client_id_file):
        with open(client_id_file, "rb") as f:
            raw = f.read()
        for enc in ["utf-8", "utf-16", "utf-16-le", "gbk"]:
            try:
                client_id = raw.decode(enc).strip()
                break
            except:
                continue
    if os.path.exists(api_key_file):
        with open(api_key_file, "rb") as f:
            raw = f.read()
        for enc in ["utf-8", "utf-16", "utf-16-le", "gbk"]:
            try:
                api_key = raw.decode(enc).strip()
                break
            except:
                continue

if not client_id or not api_key:
    print("Missing IMA credentials")
    exit(1)

# Step 1: Search for knowledge base "MD法规更新-Testing"
url = "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base"
data = json.dumps({"query": "MD法规更新", "cursor": "", "limit": 10}).encode("utf-8")

req = urllib.request.Request(
    url,
    data=data,
    headers={
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json; charset=utf-8"
    },
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

print("Knowledge base search result:")
print(json.dumps(result, indent=2, ensure_ascii=False))

# Extract knowledge base ID
kb_list = result.get("data", {}).get("kb_list", [])
kb_id = None
for kb in kb_list:
    name = kb.get("name", "")
    if "MD法规更新" in name:
        kb_id = kb.get("id")
        print(f"\nFound: {name} (ID: {kb_id})")
        break

if not kb_id:
    print("\nKnowledge base not found by name, listing all:")
    for kb in kb_list:
        print(f"  - {kb.get('name')} (ID: {kb.get('id')})")
    print("\nPlease provide the correct knowledge base name or ID.")
    exit(1)

# Step 2: Add note to knowledge base
note_id = "7453261212699682"  # From user
note_title = "医疗器械法规周报 2026-W17"

add_url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
add_data = json.dumps({
    "media_type": 11,  # Note type
    "note_info": {"content_id": note_id},
    "title": note_title,
    "knowledge_base_id": kb_id
}).encode("utf-8")

req2 = urllib.request.Request(
    add_url,
    data=add_data,
    headers={
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json; charset=utf-8"
    },
    method="POST"
)

with urllib.request.urlopen(req2) as resp2:
    result2 = json.loads(resp2.read().decode("utf-8"))

print("\nAdd knowledge result:")
print(json.dumps(result2, indent=2, ensure_ascii=False))

if result2.get("retcode") == 0:
    print("\n✅ 已成功关联到知识库「MD法规更新-Testing」")
else:
    print(f"\n❌ 失败: {result2.get('errmsg')}")
