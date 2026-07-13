#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成器 - 生成符合样例格式的 Markdown 法规追踪报告
"""

from datetime import datetime
from typing import Dict, List
from pathlib import Path


class ReportGenerator:
    """医疗器械法规追踪报告生成器"""

    # 区域旗帜（使用纯文本避免编码问题）
    REGION_FLAGS = {
        "CN": "[CN]",
        "EU": "[EU]",
        "US": "[US]",
        "CA": "[CA]"
    }

    # 区域名称
    REGION_NAMES = {
        "CN": "中国法规",
        "EU": "欧盟法规",
        "US": "美国FDA法规",
        "CA": "加拿大法规"
    }

    def __init__(self, start_date, end_date):
        """
        初始化报告生成器

        Args:
            start_date: 报告起始日期（datetime）
            end_date: 报告结束日期（datetime）
        """
        self.start_date = start_date
        self.end_date = end_date
        self.items: Dict[str, List[Dict]] = {
            "CN": [],
            "EU": [],
            "US": [],
            "CA": []
        }
        self.fetch_status: Dict[str, Dict] = {}

    def add_item(self, region: str, item: Dict):
        """添加法规条目"""
        if region in self.items:
            self.items[region].append(item)

    def set_fetch_status(self, source_id: str, status: str, message: str = ""):
        """设置抓取状态"""
        self.fetch_status[source_id] = {
            "status": status,  # success, failed, partial
            "message": message
        }

    def generate(self) -> str:
        """生成完整报告"""
        report = []

        # 1. 报告头部
        report.append(self._generate_header())

        # 2. 概览统计表
        report.append(self._generate_overview())

        # 3. 各区域详情
        report.append(self._generate_regions_detail())

        # 4. 历史记录更新
        report.append(self._generate_history())

        # 5. 抓取状态说明
        report.append(self._generate_fetch_status())

        return "\n\n".join(report)

    def _generate_header(self) -> str:
        """生成报告头部"""
        gen_date = datetime.now().strftime('%Y%m%d')
        lines = [
            f"# 医疗器械法规更新汇总（{self.start_date.strftime('%Y%m%d')}~{self.end_date.strftime('%Y%m%d')}，生成于{gen_date}）",
            "",
            f"**报告周期**: {self.start_date.strftime('%Y年%m月%d日')} ~ {self.end_date.strftime('%Y年%m月%d日')}",
            f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}",
            "**时区**: 北京时间 (UTC+8)",
            "",
            "---",
            "",
            "本报告汇集本周期内中国、欧盟、美国、加拿大等主要医疗器械市场的法规更新动态，涵盖注册审批、指导原则、标准发布、行业通知等关键信息。"
        ]
        return "\n".join(lines)

    def _generate_overview(self) -> str:
        """生成概览统计表"""
        total_items = sum(len(items) for items in self.items.values())

        lines = [
            "## 概览统计",
            "",
            "| 区域 | 本期新增 |",
            "|------|----------|"
        ]

        for region, items in self.items.items():
            region_name = self.REGION_NAMES.get(region, region)
            lines.append(f"| {region_name} | {len(items)} |")

        lines.extend([
            "",
            f"| **合计** | **{total_items}** |",
            "",
            "> 说明：以上统计基于本周期内各官方渠道公开的法规信息汇总。"
        ])

        return "\n".join(lines)

    def _generate_regions_detail(self) -> str:
        """生成各区域法规详情"""
        sections = []

        for region in ["CN", "EU", "US", "CA"]:
            if not self.items[region]:
                continue

            items = self.items[region]
            section = []

            # 区域标题
            flag = self.REGION_FLAGS.get(region, "[?]")
            name = self.REGION_NAMES.get(region, region)
            section.append(f"## {flag} {name}")
            section.append("")
            section.append(f"本期共更新 {len(items)} 条法规动态")
            section.append("")

            # 条目列表
            for i, item in enumerate(items, 1):
                section.append(self._format_item(i, item))

            sections.append("\n".join(section))

        return "\n\n".join(sections) if sections else ""

    def _format_item(self, index: int, item: Dict) -> str:
        """格式化单个法规条目"""
        tags = item.get("tags", [])
        tag_str = " ".join([f"`{tag}`" for tag in tags]) if tags else ""

        publish_date = item.get("publish_date", "未知")
        url = item.get("url", "")
        link_str = f"[查看原文]({url})" if url else ""
        summary = item.get("summary", "暂无摘要")
        impact = item.get("impact", "暂无合规影响分析")

        lines = [
            f"### {index}. {item.get('title', '无标题')} {tag_str}",
            "",
            f"- **发布机构**: {item.get('source', '未知')}",
            f"- **发布日期**: {publish_date}",
            f"- **原文链接**: {link_str}",
            "",
            f"**摘要**: {summary}",
            "",
            f"**合规影响**: {impact}",
            "",
            "---"
        ]

        return "\n".join(lines)

    def _generate_history(self) -> str:
        """生成历史记录更新部分"""
        all_items = []
        for region, items in self.items.items():
            for item in items:
                item["region"] = region
                all_items.append(item)

        if not all_items:
            return "## 历史记录更新\n\n本期无新增法规动态。"

        lines = [
            "## 历史记录更新",
            "",
            "本期新增法规条目汇总：",
            ""
        ]

        for i, item in enumerate(all_items, 1):
            region = item.get("region", "")
            region_name = self.REGION_NAMES.get(region, region)
            lines.append(f"{i}. [{region_name}] {item.get('title', '')} - {item.get('source', '')}")

        lines.extend([
            "",
            f"**本期共新增 {len(all_items)} 条法规记录**"
        ])

        return "\n".join(lines)

    def _generate_fetch_status(self) -> str:
        """生成抓取状态说明"""
        lines = ["## 抓取状态说明", ""]

        if not self.fetch_status:
            lines.append("暂无抓取状态信息。")
            return "\n".join(lines)

        success = []
        failed = []
        partial = []

        for source_id, status_info in self.fetch_status.items():
            status = status_info.get("status", "")
            msg = status_info.get("message", "")
            display = f"- **{source_id}**: {msg or status}"

            if status == "success":
                success.append(display)
            elif status == "failed":
                failed.append(display)
            else:
                partial.append(display)

        if success:
            lines.append("### 成功抓取")
            lines.extend(success)
            lines.append("")

        if partial:
            lines.append("### 部分成功")
            lines.extend(partial)
            lines.append("")

        if failed:
            lines.append("### 抓取失败")
            lines.extend(failed)
            lines.append("")

        lines.extend([
            "",
            "> **提示**: 抓取失败可能由网络问题、目标网站维护或反爬机制导致。建议稍后重试或手动访问相关网站。"
        ])

        return "\n".join(lines)

    def save(self, output_path: Path):
        """保存报告到文件"""
        content = self.generate()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path


# 测试代码
if __name__ == "__main__":
    from datetime import datetime
    from zoneinfo import ZoneInfo

    BEIJING_TZ = ZoneInfo("Asia/Shanghai")
    start = datetime(2026, 4, 10, tzinfo=BEIJING_TZ)
    end = datetime(2026, 4, 17, 23, 59, 59, tzinfo=BEIJING_TZ)

    generator = ReportGenerator(start, end)

    # 添加测试数据
    generator.add_item("CN", {
        "title": "关于公开征求《医疗器械产品技术要求编写指导原则（修订版征求意见稿）》意见的通知",
        "source": "国家药品监督管理局",
        "publish_date": "2026-04-12",
        "url": "https://www.nmpa.gov.cn/ylqx/ylqxindex.html",
        "tags": ["征求意见"],
        "summary": "国家药监局组织修订了医疗器械产品技术要求编写指导原则，现向社会公开征求意见。",
        "impact": "建议企业关注修订内容，及时反馈意见，确保产品技术要求符合新要求。"
    })

    generator.add_item("EU", {
        "title": "MDR Article 83 - PMS Plan Technical Documentation",
        "source": "European Commission",
        "publish_date": "2026-04-11",
        "url": "https://health.ec.europa.eu/medical-devices-sector/new-regulations_en",
        "tags": ["MDR", "PMS"],
        "summary": "Updated guidance on PMS plan requirements under MDR Article 83.",
        "impact": "制造商应审查并更新其PMS计划，确保符合最新指南要求。"
    })

    # 生成报告
    report = generator.generate()
    print(report)

    # 保存测试
    output = Path(__file__).parent.parent / "test_report.md"
    generator.save(output)
    print(f"\n报告已保存到: {output}")
