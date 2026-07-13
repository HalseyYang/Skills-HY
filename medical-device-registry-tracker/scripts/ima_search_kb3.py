"""搜索知识库，验证正确的ID"""
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

# 获取可添加的知识库列表
url = "https://ima.qq.com/openapi/wiki/v1/get_addable_knowledge_base_list"
payload = {"cursor": "", "limit": 50}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key,
    "Content-Type": "application/json"
}, method="POST")
print("=== get_addable_knowledge_base_list ===")
try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    print(f"retcode: {result.get('retcode')}, errmsg: {result.get('errmsg')}")
    print(f"data: {json.dumps(result.get('data', {}), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"Error: {e}")

# 搜索法规相关知识库
for query in ["法规", "MD法规", "更新"]:
    url2 = "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base"
    payload2 = {"query": query, "cursor": "", "limit": 20}
    data2 = json.dumps(payload2).encode("utf-8")
    req2 = urllib.request.Request(url2, data=data2, headers={
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json"
    }, method="POST")
    print(f"\n=== search_knowledge_base query='{query}' ===")
    try:
        with urllib.request.urlopen(req2) as resp2:
            result2 = json.loads(resp2.read().decode("utf-8"))
        print(f"retcode: {result2.get('retcode')}, errmsg: {result2.get('errmsg')}")
        for kb in result2.get("data", {}).get("info_list", []):
            print(f"  kb_id: {kb.get('id')} | name: {kb.get('name')}")
    except Exception as e:
        print(f"Error: {e}")
