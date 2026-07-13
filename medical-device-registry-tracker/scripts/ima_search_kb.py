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

url = "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base"
for query in ["MD法规更新-Testing", "Testing", "MD法规"]:
    body = json.dumps({"query": query, "cursor": "", "limit": 10}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json"
    }, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    print("Query [" + query + "]:")
    for kb in result.get("data", {}).get("info_list", []):
        print("  - " + kb["kb_name"] + " (ID: " + kb["kb_id"] + ")")
