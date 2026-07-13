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

# Add note to knowledge base
note_id = "7453261212699682"
kb_id = "ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o="
note_title = "医疗器械法规周报 2026-W17"

url = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
body = json.dumps({
    "media_type": 11,
    "note_info": {"content_id": note_id},
    "title": note_title,
    "knowledge_base_id": kb_id
}).encode("utf-8")

req = urllib.request.Request(url, data=body, headers={
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json"
}, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    print("Result:", json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("retcode") == 0 or result.get("code") == 0:
        print("OK - added to knowledge base")
    else:
        print("Failed:", result.get("msg") or result.get("errmsg"))
except Exception as e:
    print("Error:", e)
