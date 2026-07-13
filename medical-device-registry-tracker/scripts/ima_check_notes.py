"""检查知识库中的笔记列表"""
import os, json, urllib.request

config_dir = os.path.expanduser("~/.config/ima/")
for enc in ["utf-16", "utf-8", "gbk"]:
    try:
        with open(os.path.join(config_dir, "client_id"), "rb") as f:
            client_id = f.read().decode(enc).strip()
        with open(os.path.join(config_dir, "api_key"), "rb") as f:
            api_key = f.read().decode(enc).strip()
        break
    except:
        continue

print(f"Client ID: {client_id[:10]}...")
print(f"API Key: {api_key[:10]}...")

# List notes in the knowledge base
url = "https://ima.qq.com/openapi/wiki/v1/note/list_knowledge_base_notes"
data = json.dumps({
    "kb_id": "2vKqXH6BRpnhgQ2P",
    "cursor": "",
    "limit": 20
}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json"
}, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

notes = result.get("data", {}).get("info_list", [])
print(f"\n知识库中的笔记总数: {len(notes)}")
for n in notes:
    print(f"  - Title: {n.get('note_title', 'N/A')[:60]} | ID: {n.get('note_id', 'N/A')} | Time: {n.get('create_time', 'N/A')}")
