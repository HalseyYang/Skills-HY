#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗器械法规追踪器 - 主执行脚本

用法:
    python run_tracker.py                    # 执行完整追踪流程
    python run_tracker.py --dry-run         # 仅测试抓取，不上传
    python run_tracker.py --date 2026-04-10 # 指定起始日期
    python run_tracker.py --web-search-items <JSON_FILE>  # 注入 web_search 补充条目
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 导入模块
from date_utils import get_week_date_range, get_report_title
from deduplicator import RegistryDeduplicator
from report_generator import ReportGenerator
from ima_uploader import upload_to_ima
from parsers import fetch_all_sources_with_webfetch_tracking

# 导入解析器（延迟导入，因为可能需要额外依赖）
try:
    from parsers import fetch_all_sources, get_blocked_cn_sources, get_web_search_query, SOURCE_NAMES, SOURCE_URLS
    PARSERS_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] 解析器模块未完全可用: {e}")
    print("将使用基础抓取模式...")
    PARSERS_AVAILABLE = False


def run_tracker(dry_run: bool = False, reference_date: datetime = None,
                web_search_items_file: str = None):
    """
    执行法规追踪主流程

    Args:
        dry_run: 是否仅测试抓取不上传
        reference_date: 参考日期（用于测试）
        web_search_items_file: 包含 web_search 补充条目的 JSON 文件路径
    """
    print("=" * 60)
    print("[医疗器械法规追踪器]")
    print("=" * 60)
    print()

    # 1. 计算日期范围
    if reference_date:
        start_date, end_date = get_week_date_range(reference_date)
    else:
        start_date, end_date = get_week_date_range()

    print(f"[日期] 报告周期: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
    print()

    # 2. 加载配置
    config_path = SCRIPT_DIR.parent / "config" / "sources.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"[OK] 已加载 {len(config.get('regions', {}))} 个区域的法规来源配置")
    else:
        print("[WARN] 未找到来源配置文件，将使用默认配置")
        config = {"regions": {}}
    print()

    # 3. 初始化去重器
    dedup = RegistryDeduplicator()
    print(f"[INFO] 已加载 {len(dedup._registry)} 条历史推送记录")
    print()

    # 4. 初始化报告生成器
    report_gen = ReportGenerator(start_date, end_date)

    # 4.5 确保输出目录存在
    output_dir = SCRIPT_DIR / "reports"
    output_dir.mkdir(exist_ok=True)

    # 5. 抓取法规（根据解析器可用性选择模式）
    #    注意：web_fetch 类型来源由 AI web_fetch 工具处理，parsers.py 会返回 [] 并打印提示
    #    此处需要识别哪些来源需要 AI 补抓，生成清单文件供 AI 读取
    web_fetch_urls = []  # 需要 AI web_fetch 工具处理的来源清单

    if PARSERS_AVAILABLE:
        print("[抓取] 正在抓取法规信息...")
        all_items, web_fetch_sources = fetch_all_sources_with_webfetch_tracking(
            config, start_date, end_date
        )
    else:
        print("[WARN] 解析器模块不可用，跳过实际抓取")
        print("   如需完整功能，请安装依赖: pip install playwright requests beautifulsoup4")
        all_items = []
        web_fetch_sources = []

    # 5.5 输出 web_fetch 来源清单（供 AI 自动补抓）
    if web_fetch_sources:
        print()
        print("[⚠️ 需AI工具补抓] 以下来源需要使用 web_fetch 工具获取：")
        for sf in web_fetch_sources:
            print(f"  - {sf['name']} ({sf['id']})")
            print(f"    URL: {sf['url']}")
            web_fetch_urls.append({
                "source_id": sf["id"],
                "source_name": sf["name"],
                "region": sf.get("region", "unknown"),
                "url": sf["url"],
                "parser": sf.get("parser", ""),
            })

        # 保存 web_fetch 待补抓清单
        wf_pending_file = output_dir / (
            f"web_fetch_pending_{start_date.strftime('%Y%m%d')}"
            f"_{end_date.strftime('%Y%m%d')}.json"
        )
        with open(wf_pending_file, "w", encoding="utf-8") as f:
            json.dump({
                "report_period": {
                    "start": start_date.strftime('%Y-%m-%d'),
                    "end": end_date.strftime('%Y-%m-%d')
                },
                "web_fetch_sources": web_fetch_urls,
                "instructions": (
                    "AI自动化流程：对每个 web_fetch_sources 条目执行 web_fetch 工具抓取页面内容，"
                    "解析出标题、日期、URL，保存为 web_fetch_supplement_{start}_{end}.json，"
                    "然后运行 run_tracker.py --web-fetch-items <json_file>"
                )
            }, f, ensure_ascii=False, indent=2)
        print(f"\n[⚠️ 需AI工具补抓] 已保存待补抓清单: {wf_pending_file}")
        print("[⚠️ 需AI工具补抓] 请使用 web_fetch 工具补充这些来源后重新运行")
        print()

    # 6. 注入 web_search/web_fetch 补充条目（来自 AI 工具的补充抓取结果）
    web_search_additions = []
    if web_search_items_file:
        ws_path = Path(web_search_items_file)
        if ws_path.exists():
            try:
                with open(ws_path, "r", encoding="utf-8") as f:
                    ws_data = json.load(f)
                if isinstance(ws_data, list):
                    web_search_additions = ws_data
                elif isinstance(ws_data, dict):
                    # 支持两种格式：{"items": [...]} 或 {"web_fetch_sources": [...]}（带region字段）
                    web_search_additions = ws_data.get("items", ws_data.get("web_fetch_sources", []))
                print(f"[web_search/web_fetch] 已注入 {len(web_search_additions)} 条补充条目")
            except Exception as e:
                print(f"[WARN] 读取补充文件失败: {e}")
        else:
            print(f"[WARN] 补充文件不存在: {ws_path}")

    if web_search_additions:
        all_items.extend(web_search_additions)

    # 7. 输出反爬来源补充文件（供 AI 自动读取并执行 web_search）
    blocked_info = []
    if PARSERS_AVAILABLE:
        blocked_sources = get_blocked_cn_sources()
        if blocked_sources:
            print()
            print("[反爬来源] 以下国内来源需 web_search 补充：")
            for sid in blocked_sources:
                query = get_web_search_query(sid, start_date, end_date)
                name = SOURCE_NAMES.get(sid, sid)
                url = SOURCE_URLS.get(sid, "")
                print(f"  - {name}: {url}")
                print(f"    搜索建议: {query}")
                blocked_info.append({
                    "source_id": sid,
                    "source_name": name,
                    "url": url,
                    "web_search_query": query
                })

            # 保存待补充 JSON 文件
            pending_file = output_dir / (
                f"web_search_pending_{start_date.strftime('%Y%m%d')}"
                f"_{end_date.strftime('%Y%m%d')}.json"
            )
            with open(pending_file, "w", encoding="utf-8") as f:
                json.dump({
                    "report_period": {
                        "start": start_date.strftime('%Y-%m-%d'),
                        "end": end_date.strftime('%Y-%m-%d')
                    },
                    "blocked_sources": blocked_info,
                    "instructions": (
                        "AI自动化流程：对每个 blocked_sources 条目执行 web_search，"
                        "将搜索结果整理为标准条目格式，"
                        "保存为 web_search_supplement_{start}_{end}.json，"
                        "然后运行 run_tracker.py --web-search-items <json_file>"
                    )
                }, f, ensure_ascii=False, indent=2)
            print(f"\n[待补充] 已保存待补充文件: {pending_file}")
            print("[待补充] 请使用 web_search 补充后重新运行")
            print()

    # 8. 去重过滤
    new_items = dedup.filter_new(all_items)
    print(f"[统计] 抓取到 {len(all_items)} 条法规，过滤后新增 {len(new_items)} 条")
    print()

    # 9. 按区域分组并添加到报告
    for item in new_items:
        region = item.get("region", "CN")
        report_gen.add_item(region, item)

    # 10. 生成报告
    print("[生成] 正在生成报告...")
    report_content = report_gen.generate()
    report_title = get_report_title(start_date, end_date)
    print()

    # 11. 保存报告到本地（文件名包含报告周期日期 + 生成日期）
    today_str = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / (
        f"regulatory_update_{start_date.strftime('%Y%m%d')}"
        f"_{end_date.strftime('%Y%m%d')}"
        f"_generated{today_str}.md"
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[OK] 报告已保存: {output_file}")
    print()

    # 12. 更新去重记录
    for item in new_items:
        dedup.add(
            url=item.get("url"),
            title=item.get("title"),
            source=item.get("source"),
            region=item.get("region"),
            publish_date=item.get("publish_date"),
            tags=item.get("tags", [])
        )
    print(f"[OK] 已更新去重记录，当前共 {len(dedup._registry)} 条")
    print()

    # 13. 上传到 IMA（非 dry-run 模式）
    if dry_run:
        print("[Dry Run] 跳过 IMA 上传")
    else:
        print("[上传] 正在上传到 IMA...")

        # 完整上传流程：创建笔记 + 添加到知识库
        upload_result = upload_to_ima(report_content, report_title)
        if upload_result.get("success"):
            print(f"[OK] 笔记创建成功 (ID: {upload_result.get('note_id')})")
            print(f"[OK] 已添加到知识库「{upload_result.get('knowledge_base')}」")
        else:
            step = upload_result.get("step", "unknown")
            error = upload_result.get("error", "未知错误")
            print(f"[FAIL] 上传失败 (阶段: {step}): {error}")

    print()
    print("=" * 60)
    print("[完成] 执行完成")
    print("=" * 60)

    return {
        "success": True,
        "items_count": len(new_items),
        "report_file": str(output_file),
        "blocked_sources": get_blocked_cn_sources() if PARSERS_AVAILABLE else [],
        "web_search_queries": {
            sid: get_web_search_query(sid, start_date, end_date)
            for sid in (get_blocked_cn_sources() if PARSERS_AVAILABLE else [])
        }
    }


def main():
    parser = argparse.ArgumentParser(description="医疗器械法规追踪器")
    parser.add_argument("--dry-run", action="store_true", help="仅测试抓取，不上传")
    parser.add_argument("--date", type=str, help="参考日期 (YYYY-MM-DD)，用于测试")
    parser.add_argument(
        "--web-search-items", type=str, default=None,
        help="包含 web_search 补充条目的 JSON 文件路径（当国内反爬来源无法直接抓取时使用）"
    )

    args = parser.parse_args()

    reference_date = None
    if args.date:
        try:
            reference_date = datetime.strptime(args.date, "%Y-%m-%d")
            reference_date = reference_date.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
        except ValueError:
            print(f"[ERROR] 日期格式错误: {args.date}，应为 YYYY-MM-DD")
            sys.exit(1)

    result = run_tracker(
        dry_run=args.dry_run,
        reference_date=reference_date,
        web_search_items_file=args.web_search_items
    )
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
