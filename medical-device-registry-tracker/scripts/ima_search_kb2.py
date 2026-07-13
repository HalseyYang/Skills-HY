"""搜索知识库列表，获取正确的 ID"""
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

# 搜索所有知识库
url = "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base"
payload = {"query": "", "cursor": "", "limit": 50}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json"
}, method="POST")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

print(f"retcode: {result.get('retcode')}")
print(f"errmsg: {result.get('errmsg')}")
print(f"\n知识库列表:")
for kb in result.get("data", {}).get("info_list", []):
    print(f"  ID: {kb.get('id')} | Name: {kb.get('name')}")
