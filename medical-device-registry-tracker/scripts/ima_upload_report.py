"""将法规周报作为笔记添加到 IMA 知识库（正确 KB ID）"""
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

# 读取周报内容
report_path = "c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/scripts/reports/MDR_Weekly_Report_2026-W17.md"
with open(report_path, "r", encoding="utf-8") as f:
    report_content = f.read()

title = "【2026-W17】医疗器械法规周报 | 2026年4月17-24日"

# Step 1: 创建笔记
url = "https://ima.qq.com/openapi/note/v1/import_doc"
payload = {"title": title, "content": report_content, "content_format": 1}
data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json; charset=utf-8"
}, method="POST")

print("[Step 1] 创建笔记...")
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode("utf-8"))

note_id = result.get("data", {}).get("note_id", "")
print(f"  code={result.get('code')}, note_id={note_id}")

if result.get("code") == 0 and note_id:
    # Step 2: 添加到正确的知识库
    # MD法规更新汇总 kb_id: ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o=
    kb_id = "ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o="
    url2 = "https://ima.qq.com/openapi/wiki/v1/add_knowledge"
    payload2 = {
        "media_type": 11,
        "note_info": {"content_id": note_id},
        "title": title,
        "knowledge_base_id": kb_id
    }
    data2 = json.dumps(payload2, ensure_ascii=False).encode("utf-8")
    req2 = urllib.request.Request(url2, data=data2, headers={
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json; charset=utf-8"
    }, method="POST")

    print(f"\n[Step 2] 添加到「MD法规更新汇总」...")
    with urllib.request.urlopen(req2) as resp2:
        result2 = json.loads(resp2.read().decode("utf-8"))

    print(f"  retcode={result2.get('retcode')}, errmsg={result2.get('errmsg')}")
    if result2.get("retcode") == 0:
        media_id = result2.get("data", {}).get("media_id", "")
        print(f"\n成功！")
        print(f"  笔记 ID: {note_id}")
        print(f"  知识库媒体 ID: {media_id}")
    else:
        print(f"\n失败: {result2}")
else:
    print(f"\n笔记创建失败: {result}")
