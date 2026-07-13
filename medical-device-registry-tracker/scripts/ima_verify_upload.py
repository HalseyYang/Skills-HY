"""验证知识库中是否有新上传的周报"""
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

kb_id = "ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o="
url = "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list"
payload = {"knowledge_base_id": kb_id, "cursor": "", "limit": 50}
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
print(f"\n知识库「MD法规更新汇总」内容:")
for item in result.get("data", {}).get("knowledge_list", []):
    media_id = item.get("media_id", "")
    title = item.get("title", "")
    print(f"  [{media_id[:30]}...] {title}")
