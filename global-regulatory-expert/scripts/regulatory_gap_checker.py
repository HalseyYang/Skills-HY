#!/usr/bin/env python3
"""
regulatory_gap_checker.py

医疗器械法规合规差距分析脚本
用于分析 FDA 申报材料与 EU MDR 技术文档之间的差距
帮助识别可复用区域与需要差异化处理的部分

用法：
    python regulatory_gap_checker.py --fda <fda_dir> --mdr <mdr_dir> --output <output_file>
    python regulatory_gap_checker.py --config <config.json>
    python regulatory_gap_checker.py --help
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ReusabilityScore(Enum):
    """资料复用可行性评分"""
    EXTREMELY_HIGH = ("极高 (90%+)", 90)
    HIGH = ("高 (70-90%)", 75)
    MEDIUM = ("中 (40-70%)", 55)
    LOW = ("低 (10-40%)", 25)
    NOT_REUSABLE = ("不可复用", 0)

    def __init__(self, label: str, score: int):
        self.label = label
        self.score = score


class GapStatus(Enum):
    """差距状态"""
    COMPLETE = "完整"
    PARTIAL = "部分缺失"
    MISSING = "缺失"
    NOT_APPLICABLE = "不适用"


@dataclass
class DocumentGap:
    """单个文档差距"""
    document_type: str
    fda_status: GapStatus
    mdr_status: GapStatus
    reusability: ReusabilityScore
    reusability_notes: str
    gap_description: str = ""
    recommendation: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        status_icon = {
            GapStatus.COMPLETE: "[OK]",
            GapStatus.PARTIAL: "[PARTIAL]",
            GapStatus.MISSING: "[MISSING]",
            GapStatus.NOT_APPLICABLE: "[N/A]",
        }.get(self.fda_status, "[?]")

        return f"{status_icon} {self.document_type}: FDA={self.fda_status.value}, MDR={self.mdr_status.value}, 复用性={self.reusability.label}"


@dataclass
class GapAnalysisReport:
    """差距分析报告"""
    report_date: str
    fda_dir: str
    mdr_dir: str
    total_checks: int = 0
    complete_count: int = 0
    partial_count: int = 0
    missing_count: int = 0
    gaps: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "report_date": self.report_date,
            "fda_directory": self.fda_dir,
            "mdr_directory": self.mdr_dir,
            "total_checks": self.total_checks,
            "complete_count": self.complete_count,
            "partial_count": self.partial_count,
            "missing_count": self.missing_count,
            "completion_rate": f"{(self.complete_count / self.total_checks * 100):.1f}%" if self.total_checks > 0 else "0%",
            "gaps": [g.to_dict() for g in self.gaps],
            "summary": self.summary,
        }

    def to_markdown(self) -> str:
        """生成 Markdown 格式报告"""
        lines = [
            "# 医疗器械法规合规差距分析报告",
            f"\n**报告日期**: {self.report_date}",
            f"\n**FDA 文档目录**: `{self.fda_dir}`",
            f"\n**MDR 文档目录**: `{self.mdr_dir}`",
            "\n---\n",
            "\n## 总体完成情况\n",
            f"| 指标 | 数值 |",
            f"|------|------|",
            f"| 总检查项 | {self.total_checks} |",
            f"| 完整 | {self.complete_count} |",
            f"| 部分缺失 | {self.partial_count} |",
            f"| 缺失 | {self.missing_count} |",
            f"| 整体完成率 | {(self.complete_count / self.total_checks * 100):.1f}% |",
            "\n---\n",
            "\n## 详细差距分析\n",
        ]

        # 按复用可行性分组
        grouped = {}
        for gap in self.gaps:
            key = gap.reusability.label
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(gap)

        for reusability, gaps in sorted(grouped.items(), key=lambda x: -x[0][1]):
            lines.append(f"\n### 复用性：{reusability}\n")
            for gap in gaps:
                lines.append(f"\n#### {gap.document_type}\n")
                lines.append(f"- **FDA 状态**: {gap.fda_status.value}")
                lines.append(f"- **MDR 状态**: {gap.mdr_status.value}")
                lines.append(f"- **复用性评估**: {gap.reusability.label}")
                lines.append(f"- **复用说明**: {gap.reusability_notes}")
                if gap.gap_description:
                    lines.append(f"- **差距描述**: {gap.gap_description}")
                if gap.recommendation:
                    lines.append(f"- **建议**: {gap.recommendation}")
                lines.append("")

        # 汇总
        if self.summary:
            lines.append("\n---\n\n## 战略建议\n")
            for k, v in self.summary.items():
                lines.append(f"- **{k}**: {v}")

        return "\n".join(lines)


# 标准文档核查清单
STANDARD_DOCUMENT_CHECKLIST = [
    {
        "type": "器械描述与规格",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.HIGH,
        "notes": "两地描述框架相似，MDR 需要更详细的预期寿命和 state of the art 说明",
    },
    {
        "type": "适应症/预期用途",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.MEDIUM,
        "notes": "FDA indication 通常更宽，MDR indication 需更聚焦，可能需要分别版本",
    },
    {
        "type": "材料清单与化学表征",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.HIGH,
        "notes": "材料变更在两地都需评估，MDR 对 substance 评估更详细",
    },
    {
        "type": "风险管理文档 (ISO 14971)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.HIGH,
        "notes": "框架可复用，MDR 需要额外补充 GSPR 逐条核查和量化 benefit-risk",
    },
    {
        "type": "生物相容性测试 (ISO 10993)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.EXTREMELY_HIGH,
        "notes": "测试报告可直接复用两地",
    },
    {
        "type": "性能测试 (Bench Testing)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.EXTREMELY_HIGH,
        "notes": "测试报告可直接复用两地",
    },
    {
        "type": "灭菌验证",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.EXTREMELY_HIGH,
        "notes": "测试报告可直接复用，需确保 EO 残留限度分别满足两地要求",
    },
    {
        "type": "电气安全测试 (IEC 60601-1)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.EXTREMELY_HIGH,
        "notes": "测试报告可直接复用两地",
    },
    {
        "type": "EMC 测试 (IEC 60601-1-2)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.EXTREMELY_HIGH,
        "notes": "测试报告可直接复用两地",
    },
    {
        "type": "软件文档 (IEC 62304)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.HIGH,
        "notes": "文档框架可复用，MDR 对 cybersecurity 要求可能更详细",
    },
    {
        "type": "网络安全文档",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.MEDIUM,
        "notes": "两地要求方向一致，但具体控制措施有差异，建议分别准备",
    },
    {
        "type": "标签与 IFU",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.MEDIUM,
        "notes": "核心内容可参考，MDR 需要 EU 语言版本，内容可能更详细",
    },
    {
        "type": "临床评价计划 (CEP)",
        "fda_required": False,
        "mdr_required": True,
        "reusability": ReusabilityScore.NOT_REUSABLE,
        "notes": "FDA 通常不需要独立 CEP，MDR 必须有",
    },
    {
        "type": "临床评价报告 (CER)",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.LOW,
        "notes": "FDA 申报材料不能直接作为 MDR CER，必须重构",
    },
    {
        "type": "PMCF 计划",
        "fda_required": False,
        "mdr_required": True,
        "reusability": ReusabilityScore.NOT_REUSABLE,
        "notes": "FDA 无对应要求，MDR 必须有",
    },
    {
        "type": "PMS 计划",
        "fda_required": False,
        "mdr_required": True,
        "reusability": ReusabilityScore.NOT_REUSABLE,
        "notes": "FDA 无对应要求，MDR 必须有",
    },
    {
        "type": "GSPR 逐条核查",
        "fda_required": False,
        "mdr_required": True,
        "reusability": ReusabilityScore.NOT_REUSABLE,
        "notes": "FDA 无对应文件，MDR 必须有",
    },
    {
        "type": "QMS 文档",
        "fda_required": True,
        "mdr_required": True,
        "reusability": ReusabilityScore.HIGH,
        "notes": "21 CFR 820 和 ISO 13485 框架相似，可协同维护",
    },
]


def check_file_exists(base_dir: str, patterns: list[str]) -> bool:
    """检查是否存在匹配的文件"""
    base_path = Path(base_dir)
    for pattern in patterns:
        matches = list(base_path.rglob(pattern))
        if matches:
            return True
    return False


def analyze_gaps(fda_dir: str, mdr_dir: str) -> GapAnalysisReport:
    """分析 FDA 和 MDR 文档差距"""
    report = GapAnalysisReport(
        report_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        fda_dir=fda_dir,
        mdr_dir=mdr_dir,
    )

    # 文件存在性映射（用于模拟，实际需要根据真实目录结构调整）
    fda_file_patterns = {
        "器械描述与规格": ["*description*", "*specification*", "*device*"],
        "适应症/预期用途": ["*indication*", "*intended*use*", "*indications*"],
        "材料清单与化学表征": ["*material*", "*chemical*", "*characterization*"],
        "风险管理文档 (ISO 14971)": ["*risk*", "*FMEA*", "*hazard*"],
        "生物相容性测试 (ISO 10993)": ["*biocompat*", "*10993*", "*cytotox*"],
        "性能测试 (Bench Testing)": ["*performance*", "*bench*", "*testing*"],
        "灭菌验证": ["*steril*", "*bioburden*", "*SAL*"],
        "电气安全测试 (IEC 60601-1)": ["*electrical*", "*60601*", "*safety*"],
        "EMC 测试 (IEC 60601-1-2)": ["*EMC*", "*electromagnetic*", "*60601*1*2*"],
        "软件文档 (IEC 62304)": ["*software*", "*62304*", "*SaMD*"],
        "网络安全文档": ["*cyber*", "*security*", "*SBOM*"],
        "标签与 IFU": ["*label*", "*IFU*", "*instruction*"],
        "临床评价计划 (CEP)": ["*clinical*evaluation*plan*", "*CEP*"],
        "临床评价报告 (CER)": ["*clinical*evaluation*", "*CER*"],
        "PMCF 计划": ["*PMCF*", "*post*market*clinical*follow*"],
        "PMS 计划": ["*PMS*", "*post*market*surveillance*"],
        "GSPR 逐条核查": ["*GSPR*", "*general*safety*"],
        "QMS 文档": ["*QMS*", "*quality*", "*ISO*13485*", "*820*"],
    }

    for item in STANDARD_DOCUMENT_CHECKLIST:
        doc_type = item["type"]

        # 检查 FDA 文件
        fda_patterns = fda_file_patterns.get(doc_type, ["*"])
        fda_exists = check_file_exists(fda_dir, fda_patterns) if item["fda_required"] else False
        fda_status = GapStatus.COMPLETE if fda_exists else GapStatus.MISSING

        # 检查 MDR 文件
        mdr_patterns = fda_file_patterns.get(doc_type, ["*"])
        mdr_exists = check_file_exists(mdr_dir, mdr_patterns) if item["mdr_required"] else False
        mdr_status = GapStatus.COMPLETE if mdr_exists else GapStatus.MISSING

        # 生成差距描述
        gap_desc = ""
        if not fda_exists and item["fda_required"]:
            gap_desc += f"FDA 文件缺失; "
        if not mdr_exists and item["mdr_required"]:
            gap_desc += f"MDR 文件缺失; "

        # 生成建议
        if fda_status == GapStatus.COMPLETE and mdr_status == GapStatus.MISSING and item["mdr_required"]:
            recommendation = "MDR 必须文件缺失，优先准备 MDR 版本，可参考 FDA 文件框架"
        elif mdr_status == GapStatus.COMPLETE and fda_status == GapStatus.MISSING and item["fda_required"]:
            recommendation = "FDA 文件缺失，优先准备 FDA 版本"
        elif fda_status == GapStatus.MISSING and mdr_status == GapStatus.MISSING:
            recommendation = "两地文件均缺失，同时准备两地版本"
        elif fda_status == GapStatus.COMPLETE and mdr_status == GapStatus.COMPLETE:
            recommendation = "文件两地均已准备，评估复用可行性"
        else:
            recommendation = "需要进一步评估"

        gap = DocumentGap(
            document_type=doc_type,
            fda_status=fda_status,
            mdr_status=mdr_status,
            reusability=item["reusability"],
            reusability_notes=item["notes"],
            gap_description=gap_desc.rstrip("; ") if gap_desc else "两地文件均存在",
            recommendation=recommendation,
        )
        report.gaps.append(gap)
        report.total_checks += 1
        if fda_status == GapStatus.COMPLETE and mdr_status == GapStatus.COMPLETE:
            report.complete_count += 1
        elif fda_status == GapStatus.MISSING and mdr_status == GapStatus.MISSING:
            report.missing_count += 1
        else:
            report.partial_count += 1

    # 生成汇总
    report.summary = {
        "优先处理": "MDR 独有文件（CEP、CER、PMCF、PMS、GSPR）是当前差距最大的区域",
        "直接复用": "生物相容性、灭菌、电气安全、EMC 等测试报告可直接复用两地",
        "差异化处理": "临床评价、标签/IFU、网络安全等需要分别准备两地版本",
        "下一步": "建议针对 '部分缺失' 和 '缺失' 状态的文件制定补强计划",
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="医疗器械法规合规差距分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 分析指定目录
    python regulatory_gap_checker.py --fda ./fda_submission --mdr ./mdr_technical_file --output report.json

    # 使用配置文件
    python regulatory_gap_checker.py --config config.json

    # 输出 Markdown 报告
    python regulatory_gap_checker.py --fda ./fda --mdr ./mdr --format markdown --output report.md
        """,
    )

    parser.add_argument(
        "--fda",
        type=str,
        help="FDA 申报材料目录路径",
    )
    parser.add_argument(
        "--mdr",
        type=str,
        help="EU MDR 技术文档目录路径",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="gap_analysis_report.json",
        help="输出报告路径 (默认: gap_analysis_report.json)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "markdown"],
        default="json",
        help="输出格式 (默认: json)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="配置文件路径 (JSON 格式)",
    )

    args = parser.parse_args()

    # 如果提供了配置文件，从配置文件读取
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
            fda_dir = config.get("fda_directory", "")
            mdr_dir = config.get("mdr_directory", "")
            output_file = config.get("output", "gap_analysis_report.json")
            output_format = config.get("format", "json")
    else:
        if not args.fda or not args.mdr:
            parser.print_help()
            print("\n错误: 必须提供 --fda 和 --mdr 参数，或使用 --config 配置文件", file=sys.stderr)
            sys.exit(1)
        fda_dir = args.fda
        mdr_dir = args.mdr
        output_file = args.output
        output_format = args.format

    # 执行分析
    print(f"正在分析 FDA 文档目录: {fda_dir}")
    print(f"正在分析 MDR 文档目录: {mdr_dir}")
    report = analyze_gaps(fda_dir, mdr_dir)

    # 输出报告
    if output_format == "markdown":
        content = report.to_markdown()
    else:
        content = json.dumps(report.to_dict(), ensure_ascii=False, indent=2)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n分析完成！报告已保存至: {output_file}")
    print(f"\n总体完成率: {(report.complete_count / report.total_checks * 100):.1f}%")
    print(f"完整: {report.complete_count}, 部分缺失: {report.partial_count}, 缺失: {report.missing_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
