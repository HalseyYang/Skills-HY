#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://ima.qq.com/openapi/wiki/v1/search_knowledge"

KNOWLEDGE_BASES = [
    ("医疗器械", "eL8VTnWYqXBWxibVUUrgIZnuajXkF8bcFsEkVy79xXw="),
    ("医疗器械资料", "KbDCOT4c1FDrYaG6d-eV1uInSMi6O2rJ2DuQf6GZ4Ew="),
    ("医疗器械国际认证汇总知识库", "SQma_FtLh-Sh7gDyLWvIBcTZ0m_H7RdSkOTbC2vnrgo="),
    ("医疗器械国内注册汇总知识库", "_C0TjoatRKIX_5FVSjjhxwC01-ob-FepKwtdf6ctMfQ="),
    ("CE与FDA法规解读", "sulzXmP_VIFmLOvFjr_wTZLdJPUEpfpzAKV4wdmHOU0="),
    ("FDA认证汇总知识库", "M_daNwQAaqov4X8CLnjCOguVG2lqiWLO1vbxpAW3K2c="),
    ("全球产品认证合规", "PkfULCuR2PYiqiUtT2KdJrjSDQu9NCHsEdpxBB2gD8g="),
    ("医疗器械公众号文章", "VUJ-nc8nXeEQWHi9xrAIvk8VYmN8Lp39W1JCM777NQ4="),
]


def read_secret(env_name: str, path: str) -> str:
    value = os.environ.get(env_name)
    if value:
        return value.strip()
    p = Path(path).expanduser()
    return p.read_text().strip() if p.exists() else ""


def post_json(client_id: str, api_key: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=data,
        headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: ima_kb_search.py <query> [limit_per_kb] [max_total]", file=sys.stderr)
        return 2
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    max_total = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    client_id = read_secret("IMA_OPENAPI_CLIENTID", "~/.config/ima/client_id")
    api_key = read_secret("IMA_OPENAPI_APIKEY", "~/.config/ima/api_key")
    if not client_id or not api_key:
        print("Missing IMA credentials.", file=sys.stderr)
        return 1

    all_results = []
    for kb_name, kb_id in KNOWLEDGE_BASES:
        payload = {"query": query, "knowledge_base_id": kb_id, "limit": limit}
        try:
            resp = post_json(client_id, api_key, payload)
        except Exception as exc:
            all_results.append({"kb_name": kb_name, "error": str(exc)})
            continue
        if resp.get("code") != 0:
            all_results.append({"kb_name": kb_name, "error": resp.get("msg", resp)})
            continue
        for item in resp.get("data", {}).get("info_list", [])[:limit]:
            all_results.append(
                {
                    "kb_name": kb_name,
                    "title": item.get("title") or item.get("name"),
                    "media_id": item.get("media_id"),
                    "parent_folder_id": item.get("parent_folder_id"),
                    "highlight_content": item.get("highlight_content", ""),
                }
            )
            if len(all_results) >= max_total:
                break
        if len(all_results) >= max_total:
            break
    print(json.dumps(all_results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
