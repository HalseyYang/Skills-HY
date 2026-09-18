"""
generate_test_cases_excel.py - 从结构化 JSON 生成 12 列标准测试用例 Excel（V3.0）

V1.0 规则（保留）：
  - 用例仅来自标准正文条款：clause_ref 只允许数字条款号，附录编号（CC/DD 等）视为非法并拦截
  - 「条款要求」列不允许出现「§」「第 X 条」等条款号模式（避免误填）
  - 环境与判据严格取自条款原文；产品场景仅以【产品场景提示】进 lesson_learned 列

V2.0 增补（依据 YY 9706.262-2021 与企业参考版对比实证）：
  - 12 列表头冻结：列名/顺序/语义不可变更，新增能力均在现有列内消化
  - 验证方式标签：keywords 首位必须是 实测/目击检查/文档审查/风险文档审查/软件资料审查/引用
  - 条款号存在性校验：对照 _meta.clause_index，捕获 201.1 误写为 201.10 之类笔误
  - 条款覆盖连续性检查：报告标准条款索引中未被覆盖的条款（提示生成 A 类章级兜底用例）
  - 旧版引用告警：YY 0505 → YY 9706.102-2021 等
  - D 类引用展开用例缺失【限值来源】标注时告警
  - 前置条件禁止占位符（"/" "无" 等）

V2.1 增补（依据 GB 9706.224-2021 生成中断导致的"假覆盖"事故复盘）：
  - 条款覆盖间隙升级：索引已列但未生成用例且未声明豁免的条款，判定为「真实遗漏」并阻断生成，
    杜绝占位索引被静默放过、流出假覆盖 Excel；
  - 新增 _meta.exempt_clauses：显式声明"索引有但有意不生成用例"的条款及理由，未声明者不得凭空豁免；
  - 索引自身子条款连续性软检查：提示 OCR 漏提导致的子条款跳号；
  - OCR 英文残留软告警：用例文本列混入非白名单英文词（如 pering/probe/csv）时告警。

V3.0 增补（针对性优化：预期结果分条 / 步骤展开引用方法 / 步骤参数清晰）：
  - 预期结果分条性软检查：多判据建议分条（含 2 个及以上量化判据却未用 1)/2)/3) 分条）→ 告警；
  - 预期结果单条长度检查：任一条 >60 字 → 告警（判据混装）；
  - 步骤英文标准号残留软告警：test_steps 中出现 IEC/GB/YY/ISO/EN 等标准号 → 提示应展开为操作序列
    或标注【需人工复核】；
  - 步骤参数完备性软提示：步骤整体不含数字（无量值/时长/次数）→ 提示疑缺少参数。

输入 JSON 结构（list[dict]），每条 dict 对应 12 列字段：
  [
    {
      "_meta": {  // 可选，填充头部参数区；global_precondition 仅记录留存，不落 Excel
        "product": "...",
        "standard": "...",
        "author": "...",
        "reviewer": "...",
        "version": "...",
        "global_precondition": "...",
        "clause_index": ["201.4", "201.5", "201.8", ...],   // V2.0：从标准正文提取的条款清单
        "granularity": "medium",        // V2.0：coarse|medium|fine
        "expand_refs": "off"            // V2.0：on|off
      },
      "case_id": "CM-GR-00001",
      "category": "CM-GR 安规-通标",
      "keywords": "...",
      "clause_ref": "201.12.4.4.101",       # 原条款号
      "case_title": "...",
      "clause_requirement": "...",           # 不带条款号
      "precondition": "...",                 # 严格取自条款原文
      "test_steps": "1. ...\n2. ...",
      "expected_result": "...",              # 限值严格取自条款原文
      "lesson_learned": "",                  # 【需人工复核：…】/【产品场景提示：…】
      "test_result": "",
      "result_verdict": "Pending"
    },
    ...
  ]

调用：
  python generate_test_cases_excel.py <input.json> <output.xlsx> [template.xlsx]
  - template.xlsx 默认: 与 output 同目录的 template.xlsx

依赖：
  openpyxl
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: 需要 openpyxl 库。请先执行: pip install openpyxl", file=sys.stderr)
    sys.exit(1)


# ===== 样式常量 =====
HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

BODY_FONT = Font(name="微软雅黑", size=10)
BODY_ALIGN_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
CASE_ID_FONT = Font(name="Consolas", size=10)

THIN_BORDER = Border(
    left=Side(style="thin", color="BFBFBF"),
    right=Side(style="thin", color="BFBFBF"),
    top=Side(style="thin", color="BFBFBF"),
    bottom=Side(style="thin", color="BFBFBF"),
)

# 用例编号正则：XX-XX-NNNNN（如 CM-GR-00001）
CASE_ID_REGEX = re.compile(r"^[A-Z]{2,3}-[A-Z]{2,4}-\d{5}$")

# 条款号正则：仅允许正文数字条款号，如 201.12.4.4.101 / 4.3.101
# 规则：不分解附录 → 附录编号（CC.4 / CC.3.8.1 / DD.1 等）视为非法
CLAUSE_REF_REGEX = re.compile(r"^\d+(\.\d+){0,5}$")

# 附录条款号检测（用于明确报错提示）
APPENDIX_REF_REGEX = re.compile(r"^[A-Z]{2}\.?\d")

# 模糊/未明确词黑名单
FUZZY_WORDS = ["符合要求", "正常运行", "无异常", "TBD", "待定", "待确认"]

# ===== V2.0 新增常量 =====

# 验证方式标签（写入「关键词」列首位，不新增列）
# 与 references/category-code-dictionary.md §5 同步
VALIDATION_TAGS = ["实测", "目击检查", "文档审查", "风险文档审查", "软件资料审查", "引用"]

# 前置条件禁止填占位符（V1.0 实测问题：大量填 "/"）
PRECONDITION_PLACEHOLDERS = ["/", "-", "无", "N/A", "NA"]

# OCR 英文残留白名单：合法英文术语前缀（标准号、单位、通用缩写），不触发残留告警
# 注意：csv 等典型 OCR 错识词**不**在白名单内，会触发告警
_ENG_WHITELIST = {
    "IPX", "GB", "YY", "IEC", "ISO", "TBD", "ID", "OK", "NA",
    "ESD", "EMC", "ME", "PE", "PEMS", "HV", "LV", "AC", "DC",
    "RF", "USB", "SD", "LED", "LCD", "EEPROM", "RAM", "ROM",
    "MCU", "CPU", "GPS", "WIFI", "BLE", "PDF",
    "KV", "MA", "MV", "MW", "KPA", "PA", "CM", "MM", "ML", "NM", "UM",
    "DB", "HZ", "KHZ", "MHZ", "GHZ", "OHM", "WB", "J", "N", "S", "V", "A",
    "W", "G", "KG", "MG", "UG", "L", "MIN", "SEC", "APP", "TST",
}

# 规范性引用文件的旧版 → 现行版映射（详见 references/normative-ref-version-map.md）
DEPRECATED_REFS = {
    "YY 0505": "YY 9706.102-2021",
    "YY0505": "YY 9706.102-2021",
    "GB 9706.1-2007": "GB 9706.1-2020",
    "GB9706.1-2007": "GB 9706.1-2020",
    "YY/T 0316-2008": "YY/T 0316-2016",
}

# 疑似条款号笔误：正文条款号不应出现孤立的一级段（如 201.1 应为 201.10）
def looks_like_truncated_clause(ref: str) -> bool:
    """检测疑似被截断的条款号（末段为 1 位且父段存在更长同级，交由 index 校验兜底）。"""
    parts = ref.split(".")
    return len(parts) >= 2 and parts[-1] == "1" and len(parts[-2]) >= 2

# ===== V3.0 新增常量 =====

# 预期结果分条标记（严格版，用于识别"是否已分条"）：序号须出现在行首或换行后
EXPECTATION_ITEM_REGEX = re.compile(
    r"(?:^|\n)\s*(?:\d{1,2}\s*[).、）]|[一二三四五六七八九十]\s*[)、）])\s*"
)
# 预期结果分条标记（宽松版，用于"按条目切分后逐条计长"）：
# 序号可出现在行首、换行后，或紧跟在分号/句号之后（覆盖 "1) …；2) …" 同段写法）
EXPECTATION_ITEM_SPLIT_REGEX = re.compile(
    r"(?:^|\n|；|;)\s*(?:\d{1,2}\s*[).、）]|[一二三四五六七八九十]\s*[)、）])\s*"
)
# 分条数量的宽松计数（同一行内也可能用 "；2)" 连接）
EXPECTATION_ITEM_COUNT_REGEX = re.compile(r"(?:^|\n|；|;)\s*\d{1,2}\s*[).、）]\s*")

# 预期结果单条长度上限（字符）
EXPECTATION_ITEM_MAX_LEN = 60

# 预期结果收尾语（判据后补"符合即通过"式收尾，属 V3.0 明令禁止）
EXPECTATION_TAIL_PHRASES = ["符合要求即通过", "各项均满足", "各项均符合", "即为符合"]

# 测试步骤中的标准号残留（V3.0：应展开为操作序列，或标注【需人工复核】）
STD_REF_IN_STEP_REGEX = re.compile(
    r"(?:IEC|ISO|EN|GB|YY|GB/T|YY/T|IEC/TS|IEC/TR)\s*/?\s*(?:T|TS|TR)?\s*\d{3,5}",
    re.IGNORECASE,
)

# 步骤参数完备性：步骤整体无任何数字 → 疑缺参数（量值/时长/次数）
HAS_DIGIT_REGEX = re.compile(r"\d")

# 步骤序号（剥离后再判断是否含参数量值）：行首/换行处或分号后的 "1." "1)" "1、"
TEST_STEP_INDEX_REGEX = re.compile(r"(?:^|\n|；|;)\s*\d{1,2}\s*[).、）]\s*")

# 条款号残留模式（不应出现在「条款要求」列）
CLAUSE_PATTERNS = [
    re.compile(r"§\s*\d+"),          # § 4.3
    re.compile(r"第\s*[一二三四五六七八九十百零\d]+\s*条"),  # 第 5 条
    re.compile(r"条款\s*[一二三四五六七八九十百零\d]"),  # 条款 5
]


def validate_record(rec, idx, clause_index=None, warn_list=None):
    """校验单条用例记录。返回错误列表。

    V2.0:
      - clause_index: 标准条款索引集合（来自 _meta.clause_index），用于存在性校验；
      - warn_list: 外部告警收集器（旧版引用、缺失限值来源等非阻断项）。
    """
    errors = []
    warn_list = warn_list if warn_list is not None else []

    # 1. 用例编号正则
    case_id = rec.get("case_id", "")
    if not CASE_ID_REGEX.match(case_id):
        errors.append(f"[#{idx}] 用例编号格式错误: '{case_id}' (期望格式: XX-XX-NNNNN)")

    # 2. 必填列
    required = [
        "case_id", "category", "keywords", "clause_ref", "case_title",
        "clause_requirement", "precondition", "test_steps", "expected_result",
    ]
    for field in required:
        if not str(rec.get(field, "")).strip():
            errors.append(f"[#{idx}] 必填列 '{field}' 为空")

    # 3. clause_ref 格式校验（仅正文条款号）
    clause_ref = str(rec.get("clause_ref", "")).strip()
    if clause_ref:
        if APPENDIX_REF_REGEX.match(clause_ref):
            errors.append(
                f"[#{idx}] 条款（clause_ref）含附录编号: '{clause_ref}' "
                f"(规则不分解附录，请仅保留正文条款用例，如 201.12.4.4.101)"
            )
        elif not CLAUSE_REF_REGEX.match(clause_ref):
            errors.append(
                f"[#{idx}] 条款（clause_ref）格式错误: '{clause_ref}' "
                f"(期望正文数字条款号，如 201.12.4.4.101)"
            )

    # 4. 模糊预期结果
    expected = str(rec.get("expected_result", ""))
    for word in FUZZY_WORDS:
        if word in expected:
            errors.append(f"[#{idx}] 预期结果含模糊词: '{word}' (位置: {expected.find(word)})")
            break

    # 5. 条款要求列不应残留条款号
    clause_req = str(rec.get("clause_requirement", ""))
    for pat in CLAUSE_PATTERNS:
        m = pat.search(clause_req)
        if m:
            errors.append(
                f"[#{idx}] 条款要求列不应出现条款号残留: '{m.group(0)}' "
                f"（条款号请填到「条款」列）"
            )
            break

    # 6. 条款要求/前置条件/测试步骤 是否含 TBD/待定
    for col in ["clause_requirement", "precondition", "test_steps"]:
        val = str(rec.get(col, ""))
        for word in ["TBD", "待定", "待确认"]:
            if word in val:
                errors.append(f"[#{idx}] {col} 含未明确词: '{word}'")
                break

    # ===== V2.0 新增校验 =====

    # 7. 关键词首位必须是验证方式标签（表头冻结，证据类型靠标签承载）
    keywords = str(rec.get("keywords", "")).strip()
    if keywords:
        first_tag = keywords.split(",")[0].strip()
        if first_tag not in VALIDATION_TAGS:
            errors.append(
                f"[#{idx}] 关键词首位不是合法的验证方式标签: '{first_tag}' "
                f"(合法值: {' / '.join(VALIDATION_TAGS)})"
            )

    # 8. 前置条件禁止占位符
    precond = str(rec.get("precondition", "")).strip()
    if precond in PRECONDITION_PLACEHOLDERS:
        errors.append(
            f"[#{idx}] 前置条件为占位符 '{precond}'，必须填写条款专属条件或文档类型"
        )

    # 9. 条款号存在性校验（对照 _meta.clause_index）
    clause_ref = str(rec.get("clause_ref", "")).strip()
    if clause_index is not None and clause_ref:
        if clause_ref not in clause_index:
            hint = ""
            if looks_like_truncated_clause(clause_ref):
                hint = " （疑似截断笔误，请核对是否漏写末位数字）"
            errors.append(
                f"[#{idx}] 条款号 '{clause_ref}' 不存在于标准条款索引中{hint}"
            )

    # 10. 旧版规范性引用告警（不阻断）
    if warn_list is not None:
        for col in ["clause_requirement", "precondition", "test_steps",
                    "expected_result", "lesson_learned"]:
            val = str(rec.get(col, ""))
            for old_ref, new_ref in DEPRECATED_REFS.items():
                if old_ref in val:
                    warn_list.append(
                        f"[#{idx}] {col} 引用了旧版标准 '{old_ref}'，建议替换为 '{new_ref}'"
                    )

    # 11. D 类引用展开：lesson_learned 应标注【限值来源】
    #     排除 A 类章级兜底（关键词含"通用标准/通标/章"）：其预期结果本就含"第 X 章"字样，
    #     并非展开所得限值，不应强制标注【限值来源】
    kw_tag = keywords.split(",")[0].strip() if keywords else ""
    expected = str(rec.get("expected_result", ""))
    lesson = str(rec.get("lesson_learned", ""))
    _is_class_a_umbrella = ("通用标准" in expected or "通标" in expected
                            or re.search(r"第\s*\d+\s*章", expected) is not None)
    has_numeric_limit = any(ch.isdigit() for ch in expected)
    if (has_numeric_limit and kw_tag == "引用" and not _is_class_a_umbrella
            and "限值来源" not in lesson):
        warn_list.append(
            f"[#{idx}] 疑似引用展开用例但未标注【限值来源：<引用标准号> <条款号>】"
        )

    # 12. OCR 英文残留软告警（扫描版 OCR 可能混入错识词，如 pering/probe/csv）
    #     匹配策略（V3.0 修正）：白名单**精确匹配**（原为前缀匹配，导致 'pering' 误配 'PE' 而漏报）；
    #     另放行"计量单位+数字"形式（如 5kV / 100mA / 60Hz）与"标准号"形式（GB/T、IEC 62556）
    if warn_list is not None:
        _eng_text = " ".join(str(rec.get(col, "")) for col in
                             ["case_title", "clause_requirement", "precondition",
                              "test_steps", "expected_result", "lesson_learned"])
        # 剥离标准号与带数字单位，避免误报
        _eng_text_clean = STD_REF_IN_STEP_REGEX.sub(" ", _eng_text)
        _eng_text_clean = re.sub(r"\d+\s*(?:[A-Za-z]{1,4})\b", " ", _eng_text_clean)
        for _tok in re.findall(r"[A-Za-z]{3,}", _eng_text_clean):
            if _tok.upper() not in _ENG_WHITELIST:
                warn_list.append(
                    f"[#{idx}] 文本列疑似含 OCR 残留英文词: '{_tok}' "
                    f"（如非合法术语请修正；GB/T、IPX7、kV 等单位与标准号不在告警范围）"
                )
                break

    # ===== V3.0 新增软校验（warn 级，不阻断） =====

    if warn_list is not None:
        expected = str(rec.get("expected_result", ""))
        steps = str(rec.get("test_steps", ""))
        lesson = str(rec.get("lesson_learned", ""))

        # C 类文档/记录审查用例：预期结果为"条目清单式"，天然较长且步骤无需量值参数 → 豁免长度/参数检查
        _is_doc_review = kw_tag in ("文档审查", "风险文档审查", "软件资料审查")

        # 13. 预期结果分条性：含多条判据（≥1 个分号）却未按 1) 2) 3) 分条 → 告警
        _item_count = len(EXPECTATION_ITEM_COUNT_REGEX.findall(expected))
        _has_numeric = bool(re.search(r"\d", expected))
        _multi_sep = expected.count("；") + expected.count(";")
        if _has_numeric and _item_count < 2 and _multi_sep >= 1:
            warn_list.append(
                f"[#{idx}] 预期结果疑似未分条（含多条判据但无 1) 2) 3) 编号），"
                f"建议按 SKILL §四步 4.2 分条呈现"
            )

        # 14. 预期结果单条长度：任一条 >60 字 → 告警（C 类条目清单豁免）
        #     切分用宽松版正则，兼容 "1) …；2) …" 同段写法（V3.0 修正：原用严格版导致整段被判为一条而误报）
        _items = [it.strip() for it in EXPECTATION_ITEM_SPLIT_REGEX.split(expected) if it.strip()]
        if _items and not _is_doc_review:
            _long = [it for it in _items if len(it) > EXPECTATION_ITEM_MAX_LEN]
            if _long:
                warn_list.append(
                    f"[#{idx}] 预期结果存在单条 >{EXPECTATION_ITEM_MAX_LEN} 字（疑判据混装），"
                    f"请继续拆分：'{_long[0][:40]}…'"
                )

        # 15. 预期结果收尾语（V3.0 明令禁止）
        for _tail in EXPECTATION_TAIL_PHRASES:
            if _tail in expected:
                warn_list.append(
                    f"[#{idx}] 预期结果含被禁止的收尾语 '{_tail}'，判据本身已含合格边界，请删除"
                )
                break

        # 16. 测试步骤中的标准号残留（路径 A 应已展开为操作序列）
        _std_hits = STD_REF_IN_STEP_REGEX.findall(steps)
        if _std_hits and "需人工复核" not in lesson:
            warn_list.append(
                f"[#{idx}] 测试步骤出现标准号 '{_std_hits[0]}'：若方法已收录于 "
                f"test-method-toolkit.md 应展开为操作序列；若未收录须在「经验教训」列标注"
                f"【需人工复核：<标准号> 方法细节未展开…】"
            )

        # 17. 步骤参数完备性：剥离步骤序号后仍无任何数字 → 疑缺参数（C 类文档核对无需量值，豁免）
        _steps_body = TEST_STEP_INDEX_REGEX.sub("", steps)
        _steps_body = _steps_body.replace("步骤", "")
        if steps and not _is_doc_review and not HAS_DIGIT_REGEX.search(_steps_body):
            warn_list.append(
                f"[#{idx}] 测试步骤不含任何量值/时长/次数（仅有序号），疑缺少参数，"
                f"请对照 clause-splitting-rules.md §2.8 七类信息表回补"
            )

    return errors


def fill_row(ws, row_idx, rec):
    """填充一行用例到指定 sheet。"""
    data = [
        rec.get("case_id", ""),
        rec.get("category", ""),
        rec.get("keywords", ""),
        rec.get("clause_ref", ""),  # 原条款号
        rec.get("case_title", ""),
        rec.get("clause_requirement", ""),  # 不含条款号
        rec.get("precondition", ""),
        rec.get("test_steps", ""),
        rec.get("expected_result", ""),
        rec.get("lesson_learned", ""),
        rec.get("test_result", ""),
        rec.get("result_verdict", "Pending"),
    ]

    for col_idx, value in enumerate(data, start=1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.font = CASE_ID_FONT if col_idx == 1 else BODY_FONT
        cell.alignment = BODY_ALIGN_WRAP
        cell.border = THIN_BORDER


def generate_excel(input_json: Path, output_xlsx: Path, template_xlsx: Path):
    """主流程。"""
    # 1. 读取 JSON
    with open(input_json, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        print("ERROR: JSON 根节点必须是 list", file=sys.stderr)
        sys.exit(1)

    # 2. 提取 _meta（含 clause_index 条款索引）
    meta = next((r["_meta"] for r in records if r.get("_meta")), None) or {}
    clause_raw = meta.get("clause_index")
    clause_index = set(str(c).strip() for c in clause_raw) if clause_raw else None

    if clause_index is None:
        print("WARN: 未提供 _meta.clause_index，条款号存在性与连续性校验降级跳过")

    # 2A. 校验所有记录
    all_errors = []
    all_warnings = []
    for idx, rec in enumerate(records, start=1):
        # _meta 字段不参与单条校验
        if rec.get("_meta"):
            continue
        errs = validate_record(rec, idx, clause_index=clause_index, warn_list=all_warnings)
        all_errors.extend(errs)

    if all_errors:
        print(f"ERROR 数据校验失败（共 {len(all_errors)} 条错误）：")
        for e in all_errors:
            print("  - " + e)
        print("\n请修正 JSON 后重试。")
        sys.exit(1)

    if all_warnings:
        print(f"WARN 非阻断告警（共 {len(all_warnings)} 条）：")
        for w in all_warnings:
            print("  - " + w)

    # 2B. 条款覆盖间隙（真实遗漏 vs 有意豁免）检查 —— V2.1 修复"占位索引被静默放过"
    if clause_index:
        covered = set()
        for rec in records:
            if rec.get("_meta"):
                continue
            ref = str(rec.get("clause_ref", "")).strip()
            if ref:
                covered.add(ref)
        # 已声明豁免：仅在 _meta.exempt_clauses 给出理由的条款方可豁免，不得凭空豁免
        exempt_raw = meta.get("exempt_clauses") or {}
        exempt = {str(k).strip(): str(v).strip() for k, v in exempt_raw.items()}
        missing = clause_index - covered
        real_missing = sorted(missing - set(exempt.keys()))
        # 父前缀过滤：未覆盖条款若是已覆盖条款的祖先（中间章标题/父条款已由子条款覆盖），不视为遗漏
        #   例：索引含 201.12.1（父标题）而用例覆盖 201.12.1.101，则 201.12.1 不算真实遗漏
        covered_prefixes = set()
        for _c in covered:
            _p = _c.split(".")
            for _i in range(1, len(_p)):
                covered_prefixes.add(".".join(_p[:_i]))
        real_missing = sorted(m for m in real_missing if m not in covered_prefixes)
        if exempt:
            print(f"INFO 已声明豁免条款（索引列但无用例，已附理由）：{len(exempt)} 条")
            for cl, reason in sorted(exempt.items()):
                print(f"     - {cl}: {reason}")
        if real_missing:
            print(f"ERROR 条款真实遗漏（索引已列但未生成用例且未声明豁免，共 {len(real_missing)} 条）：")
            for m in real_missing[:80]:
                print("     - " + m)
            if len(real_missing) > 80:
                print(f"     ...（另有 {len(real_missing) - 80} 条）")
            print(f"     涉及章号：{', '.join(sorted({c.split('.')[0] for c in real_missing}))}")
            print("     这些条款不会进入 Excel（已阻断生成），请补用例或将其填入 _meta.exempt_clauses 并附理由。")
            sys.exit(1)
        elif not exempt:
            print("OK 条款覆盖连续性检查：标准条款索引已被全部覆盖（无豁免）")
        else:
            print("OK 条款覆盖连续性检查：索引中未豁免条款已被全部覆盖")

    # 2C. 索引自身子条款连续性软检查（WARN，提示 OCR 漏提 / 标准本身跳号）
    if clause_index:
        from collections import defaultdict
        groups = defaultdict(list)
        for c in clause_index:
            parts = str(c).split(".")
            if len(parts) >= 2 and parts[-1].isdigit():
                groups[".".join(parts[:-1])].append(int(parts[-1]))
        for parent, nums in groups.items():
            ns = sorted(set(nums))
            gaps = []
            for a, b in zip(ns, ns[1:]):
                if b - a > 1:
                    gaps.extend(range(a + 1, b))
            if gaps:
                print(f"WARN 索引子条款疑似跳号（父 {parent}.）：缺失 "
                      f"{parent}.{gaps[0]}..{parent}.{gaps[-1]} "
                      f"（可能 OCR 漏提或标准本身跳号，请人工核对）")

    # 3. 加载模板（在 init_workbook 基础上追加数据）
    if not template_xlsx.exists():
        print(f"ERROR 模板不存在: {template_xlsx}", file=sys.stderr)
        print("请先运行: python init_workbook.py <template.xlsx>")
        sys.exit(1)

    wb = load_workbook(template_xlsx)
    ws = wb["测试用例"]

    # 4. 定位数据起始行（表头在第 7 行，数据从第 8 行起）
    DATA_START_ROW = 8

    # 5. 过滤掉 _meta 字段并填充数据
    data_records = [r for r in records if not r.get("_meta")]
    for i, rec in enumerate(data_records):
        fill_row(ws, DATA_START_ROW + i, rec)
        # 自适应行高（粗略）
        max_lines = max(
            len(str(rec.get("clause_requirement", "")).splitlines()),
            len(str(rec.get("test_steps", "")).splitlines()),
            len(str(rec.get("expected_result", "")).splitlines())
            + len(str(rec.get("lesson_learned", "")).splitlines()) * 0.5
            + 1,
        )
        ws.row_dimensions[DATA_START_ROW + i].height = max(30, min(20 * max_lines, 240))

    # 6. 更新筛选范围
    last_row = DATA_START_ROW + len(data_records) - 1
    ws.auto_filter.ref = f"A7:L{last_row}"

    # 7. 填充头部参数区（如果 JSON 中带 _meta 字段）
    if meta:
        for i, key in enumerate(["product", "standard", "author", "reviewer", "version"], start=1):
            if key in meta:
                ws.cell(row=i, column=2, value=meta[key]).font = BODY_FONT

    # 8. 保存
    wb.save(output_xlsx)
    print(f"OK 已生成 Excel (V2.0): {output_xlsx}")
    print(f"   用例数: {len(data_records)} 条")
    print(f"   数据行: 第 {DATA_START_ROW} 行 ~ 第 {last_row} 行")

    # 9. V2.0 交付摘要统计
    tag_dist = Counter()
    cat_dist = Counter()
    for rec in data_records:
        kw = str(rec.get("keywords", "")).strip()
        tag = kw.split(",")[0].strip() if kw else "(缺失)"
        tag_dist[tag] += 1
        cat_dist[str(rec.get("category", "")).split(" ")[0]] += 1

    print("   【V2.0 自检统计】")
    print(f"   验证方式分布: {dict(tag_dist)}")
    print(f"   测试模块分布: {dict(cat_dist)}")
    if meta.get("granularity"):
        print(f"   粒度: {meta['granularity']} / 引用展开: {meta.get('expand_refs', 'off')}")


def main():
    if len(sys.argv) < 3:
        print("用法: python generate_test_cases_excel.py <input.json> <output.xlsx> [template.xlsx]")
        print("  template.xlsx 默认: 与 output 同目录的 template.xlsx")
        sys.exit(1)

    input_json = Path(sys.argv[1])
    output_xlsx = Path(sys.argv[2])
    template_xlsx = (
        Path(sys.argv[3]) if len(sys.argv) > 3
        else output_xlsx.parent / "template.xlsx"
    )

    if not input_json.exists():
        print(f"ERROR 输入 JSON 不存在: {input_json}", file=sys.stderr)
        sys.exit(1)

    generate_excel(input_json, output_xlsx, template_xlsx)


if __name__ == "__main__":
    main()
