"""
init_workbook.py - 初始化标准解读 skill 的 Excel 模板（V1.0）

功能：
  1. 创建 12 列表头 + 样式（加粗、深蓝底白字、冻结首行、列宽、自动换行）
  2. 创建「字典」sheet（含产品代码 × 测试模块代码 = 88 项笛卡尔积）
  3. 创建工作表头部参数区（产品简称、引用标准、编制人、审核人、版本）
  4. 在「测试项目分类」「结果判定」两列加数据校验下拉

V1.0 说明：
  - 用例仅由正文条款分解，附录（AA/BB/CC/DD）不生成用例（SKILL.md 红线）
  - 第 4 列「条款」填原条款号（列宽 16）

调用：
  python init_workbook.py <output.xlsx>

依赖：
  openpyxl
"""

import sys
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: 需要 openpyxl 库。请先执行: pip install openpyxl", file=sys.stderr)
    sys.exit(1)


# ===== 1. 字典定义（与 references/category-code-dictionary.md 同步）=====

PRODUCT_CODES = [
    ("CM", "通用"),
    ("RF", "射频"),
    ("MF", "超声"),
    ("LT", "光疗"),
    ("LS", "激光"),
    ("PL", "等离子"),
    ("IPL", "光子"),
    ("HA", "家用"),
]

TEST_MODULE_CODES = [
    ("AP", "外观"),
    ("ST", "结构"),
    ("HW", "硬件"),
    ("SW", "软件"),
    ("PF", "性能"),
    ("RL", "可靠性"),
    ("GR", "安规-通标"),
    ("PR", "安规-专标"),
    ("FT", "功能"),
    ("ESD", "EMC（静电）"),
    ("EMC", "EMC"),
]

RESULT_VERDICTS = ["Pass", "Fail", "Blocked", "N/A", "Pending"]

# ===== V2.0：验证方式标签字典（6 项，写入「关键词」列首位，不新增列）=====
# 与 references/category-code-dictionary.md §5 同步
VALIDATION_TAGS = [
    ("实测", "仪器测量 / 环境试验 / 通电操作"),
    ("目击检查", "外观、标识、显示可读性现场目测"),
    ("文档审查", "核对使用说明书 / 技术说明书条目完备性"),
    ("风险文档审查", "核对风险管理文档条目完备性"),
    ("软件资料审查", "核对软件生存周期 / PEMS 文档"),
    ("引用", "指向引用标准章节（A 类章级兜底）"),
]


# ===== 2. 样式定义 =====

HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

BODY_FONT = Font(name="微软雅黑", size=10)
BODY_ALIGN_WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
BODY_ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

CASE_ID_FONT = Font(name="Consolas", size=10)

THIN_BORDER = Border(
    left=Side(style="thin", color="BFBFBF"),
    right=Side(style="thin", color="BFBFBF"),
    top=Side(style="thin", color="BFBFBF"),
    bottom=Side(style="thin", color="BFBFBF"),
)

PARAM_HEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
PARAM_LABEL_FONT = Font(name="微软雅黑", size=10, bold=True, color="1F4E79")


# ===== 3. 12 列表头 =====

COLUMNS = [
    "用例编号",
    "测试项目分类",
    "关键词",
    "条款",  # 填原条款号
    "用例标题",
    "条款要求",  # 不含条款号
    "前置条件",
    "测试步骤",
    "预期结果",
    "经验教训",  # 承载人工复核 + 产品场景提示 + 踩坑要点
    "测试结果",
    "结果判定",
]

# (列字母, 宽度字符数)
COL_WIDTHS = {
    "A": 16,  # 用例编号
    "B": 22,  # 测试项目分类
    "C": 20,  # 关键词
    "D": 16,  # 条款（原条款号）
    "E": 32,  # 用例标题
    "F": 46,  # 条款要求
    "G": 28,  # 前置条件
    "H": 46,  # 测试步骤
    "I": 36,  # 预期结果
    "J": 38,  # 经验教训
    "K": 28,  # 测试结果
    "L": 10,  # 结果判定
}


def build_dictionary_sheet(wb):
    """创建「字典」sheet，含 88 项产品×模块笛卡尔积。"""
    ws = wb.create_sheet("字典")
    ws.append(["组合代码", "组合名称"])
    for cell in ws[1]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER

    for prod_code, prod_name in PRODUCT_CODES:
        for mod_code, mod_name in TEST_MODULE_CODES:
            combo_code = f"{prod_code}-{mod_code}"
            combo_name = f"{prod_code}-{mod_code} {mod_name}"
            ws.append([combo_code, combo_name])

    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 30

    # --- V2.0：验证方式标签区（D/E 列，与产品×模块区分开）---
    ws.cell(row=1, column=4, value="验证方式标签")
    ws.cell(row=1, column=5, value="标签含义")
    for cell in (ws.cell(row=1, column=4), ws.cell(row=1, column=5)):
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER

    for i, (tag, desc) in enumerate(VALIDATION_TAGS, start=2):
        ws.cell(row=i, column=4, value=tag)
        ws.cell(row=i, column=5, value=desc)

    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 38
    ws.freeze_panes = "A2"
    return ws


def build_main_sheet(wb, dict_sheet):
    """创建主用例 sheet，含 12 列表头 + 样式 + 下拉。"""
    ws = wb.create_sheet("测试用例", 0)  # 放最前

    # 3.1 工作表头部参数区（前 5 行）
    params = [
        ("产品/项目简称：", ""),
        ("引用标准：", ""),
        ("编制人：", ""),
        ("审核人：", ""),
        ("版本：", ""),
    ]
    for i, (label, _) in enumerate(params, start=1):
        cell = ws.cell(row=i, column=1, value=label)
        cell.font = PARAM_LABEL_FONT
        cell.fill = PARAM_HEADER_FILL
        cell.alignment = Alignment(horizontal="right", vertical="center")

    # 3.2 12 列表头（第 7 行，预留 1 行空行后）
    HEADER_ROW = 7
    for col_idx, col_name in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=HEADER_ROW, column=col_idx, value=col_name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = THIN_BORDER

    # 3.3 列宽
    for col_letter, width in COL_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

    # 3.4 行高
    ws.row_dimensions[HEADER_ROW].height = 28

    # 3.5 冻结首行（表头下方）
    ws.freeze_panes = "A8"

    # 3.6 数据校验下拉：测试项目分类
    # 字典 sheet 共 88 项 + 表头 1 行 = 89 行，A2:A89 为组合代码
    dict_max_row = len(PRODUCT_CODES) * len(TEST_MODULE_CODES) + 1  # 89
    combo_list = f"=字典!$A$2:$A${dict_max_row}"

    cat_dv = DataValidation(
        type="list",
        formula1=combo_list,
        allow_blank=True,
        showDropDown=False,  # False = 显示下拉箭头
    )
    cat_dv.error = "请从字典中选择合法的测试项目分类（产品代码-测试模块代码）"
    cat_dv.errorTitle = "无效分类"
    cat_dv.prompt = "格式：XX-XX，如 CM-GR、RF-FT"
    cat_dv.promptTitle = "测试项目分类"
    ws.add_data_validation(cat_dv)
    cat_dv.add(f"B8:B1000")

    # 3.7 数据校验下拉：结果判定
    verdict_dv = DataValidation(
        type="list",
        formula1='"' + ",".join(RESULT_VERDICTS) + '"',
        allow_blank=True,
        showDropDown=False,
    )
    verdict_dv.error = "请从列表中选择：Pass / Fail / Blocked / N/A / Pending"
    verdict_dv.errorTitle = "无效判定"
    ws.add_data_validation(verdict_dv)
    verdict_dv.add(f"L8:L1000")

    # 3.8 全表筛选
    ws.auto_filter.ref = f"A{HEADER_ROW}:L{HEADER_ROW}"

    return ws


def main():
    if len(sys.argv) < 2:
        print("用法: python init_workbook.py <output.xlsx>")
        sys.exit(1)

    output_path = Path(sys.argv[1])

    wb = Workbook()
    # 删除默认 sheet
    wb.remove(wb.active)

    # 先建字典 sheet（让主 sheet 引用）
    dict_ws = build_dictionary_sheet(wb)
    main_ws = build_main_sheet(wb, dict_ws)

    # 默认 sheet 顺序：测试用例 -> 字典
    wb.save(output_path)
    print(f"OK 已创建 Excel 模板 (V2.0): {output_path}")
    print(f"   12 列表头已冻结（列名/顺序/语义不可变更）")
    print(f"   字典项数: {len(PRODUCT_CODES) * len(TEST_MODULE_CODES)} 项产品×模块组合 + {len(VALIDATION_TAGS)} 项验证方式标签")
    print(f"   数据校验: 测试项目分类(下拉引用字典)、结果判定({', '.join(RESULT_VERDICTS)})")


if __name__ == "__main__":
    main()
