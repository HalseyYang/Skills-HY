# -*- coding: utf-8 -*-
"""
【第 1 轮】检索词与检索式文档生成器（产品无关）
=================================================
skill：文献检索词与检索式生成skill
只改下面 CONFIG 区，其余全部自动生成。

产出：Word 文档，含单元1/单元2 词表、7 个数据库可直接复制的检索式、
命中数记录表、一轮判定表、查全验证基线表。

下一轮：跑完一轮并回填命中数后，若判定「过宽」，复制本脚本的 CONFIG
到 gen_round2_doc.py，单元 1/2 一字不改，只追加单元 3（使用部位）。

用法：
    python gen_round1_doc.py
如需换产品，修改 CONFIG 后另存脚本或直接改本文件。
"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ======================================================================
#                              CONFIG 区
# ======================================================================

OUT = r"C:/Users/lenovo/Desktop/一轮检索词与检索式_workbuddy版本.docx"

PRODUCT_CN   = "（产品中文名）"          # 封面主标题
SUBTITLE     = "一轮检索词与检索式（简化版）"
SCOPE_NOTE   = "单元 1（产品/技术名）AND 单元 2（厂家名称）　各库一条组合式"

# ---- 单元 1：产品 / 技术名 ---------------------------------------------
# CN_TERM：中文最大公因式，一个词覆盖所有中文产品名写法（仅中文三库使用）
CN_TERM      = "（中文通用词）"
CN_TERM_NOTE = "一个词覆盖该类产品全部中文写法"
CN_ALIAS     = ""    # 中文产品别名（可选，用于维普二轮示例；留空则只用 CN_TERM）

# CN_TERMS：中文【产品名族】。当一个最大公因式无法覆盖时（如国产同类产品命名不统一，
#           五种叫法的共同词素过宽、单独使用噪声过大），改用本列表做 OR 枚举。
#           留空 [] 则自动回退到上面的单值 CN_TERM（默认情形，与既有产品兼容）。
CN_TERMS     = []    # 例：[("口腔生物膜", "本品注册名"), ("口腔修复膜", "同类产品注册名"), ...]

# ★ KEEP_ALWAYS：子串覆盖去重的白名单。凡「能在注册证 / 指导原则 / 已发表文献里
#   指认出来源」的产品名一律写进来（官方通用名、CMDE 品名举例、同类注册名、实证异写）。
#   原因：自动去重按连续子串删词，而部分中文库（知网 FT）按分词命中，
#   删掉这些名会整批漏检——召回损失远大于检索式多几个词的代价。
#   例：KEEP_ALWAYS = ["口腔修复膜", "可吸收口腔修复膜", "口腔可吸收修复膜"]
KEEP_ALWAYS = []

# BRAND_TERMS：英文品牌变体 / 技术特征词，全库使用（含连字符、连写等各种写法）
BRAND_TERMS  = [
    ("（品牌词根-BrandRoot）",   "覆盖全部带该品牌词根的产品英文全名，故不再单列全名"),
    ("（品牌连写-BrandX）",     "合并连写写法"),
    ("（技术特征词-cooled-tip）", "技术文献中的通用写法（不依赖品牌名）"),
]

# PREFIX_TERMS：需前缀收敛的技术词（中文库加尾空格、Embase 加 *、维普不加引号模糊、PubMed 按词索引）
PREFIX_TERMS = [
    ("（技术词-radiofrequency）", "★ 前缀匹配，一条覆盖全部派生词组"),
    ("（缩写-RF）",               "★ 前缀匹配，注意缩写歧义"),
]

# ---- 单元 2：厂家名称（含并购史）---------------------------------------
# 每个时期：period / en 列表 / cn 列表 / note
MANUFACTURERS = [
    {"period": "（时期1）", "en": ["（英文实体名）", "（英文子品牌）"],
     "cn": ["（中文译名1）", "（中文译名2）"], "note": "（沿革说明）"},
    {"period": "（时期2）", "en": ["（英文实体名）"], "cn": ["（中文译名）"],
     "note": "（沿革说明）"},
    {"period": "（时期3·现名）", "en": ["（英文现名）"], "cn": ["（中文现名）"],
     "note": "（沿革说明）"},
]

# ---- 二轮加严用：限定词（字段仍用全文，只加词不切字段）-------------------
# 路径 A：使用部位 / 适应证词（优先、无损）
SITE_TERMS_CN = ["（部位词1）", "（部位词2）", "（部位词3）"]
SITE_TERMS_EN = ["（site term 1）", "（site term 2）", "（site term 3）"]

# 路径 B：产品名加严（A 用尽后再用、有损；用 AND 叠加，不替换原词）
STRICT_CN     = []    # 中文逐级收窄，如 ["射频消融", "冷循环射频消融"]
STRICT_EN     = []    # 英文完整产品名，如 ["BrandRoot RFA System", "BrandRoot RF Ablation System"]

# 路径 B4：术式 / 路径词（可选）
PROCEDURE_CN  = []    # 如 ["经皮", "腹腔镜"]
PROCEDURE_EN  = []    # 如 ["percutaneous", "laparoscopic"]

# ---- 查全验证基线文献 ---------------------------------------------------
GOLD_REFS = ["（金标准文献 1）", "（金标准文献 2）", "（金标准文献 3）"]
GOLD_SRC  = "（金标准文献来源，如说明书第 5 章）"

# ======================================================================
#                          以下为生成逻辑，一般无需修改
# ======================================================================

ORANGE = RGBColor(0xE0, 0x8A, 0x2E); BROWN  = RGBColor(0xB5, 0x60, 0x0F)
CREAM  = RGBColor(0xFC, 0xF3, 0xE4); INK    = RGBColor(0x33, 0x33, 0x33)
GRAY   = RGBColor(0x5A, 0x5A, 0x5A); WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
FONT   = "微软雅黑"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.3)
sec.top_margin = Cm(2.3); sec.bottom_margin = Cm(2.1)

st = doc.styles['Normal']
st.font.name = FONT; st.font.size = Pt(10.5); st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
st.paragraph_format.line_spacing = 1.4
st.paragraph_format.space_after = Pt(4)


def set_run(r, size=10.5, bold=False, color=INK, font=FONT, italic=False):
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color; r.font.name = font
    r._element.rPr.rFonts.set(qn('w:eastAsia'), font)
    r._element.rPr.rFonts.set(qn('w:ascii'), font)
    r._element.rPr.rFonts.set(qn('w:hAnsi'), font)
    return r


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)


def cell_text(cell, text, size=9.5, bold=False, color=INK, align=None, mono=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if align is not None: p.alignment = align
    for i, ln in enumerate(str(text).split("\n")):
        if i > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_after = Pt(2); p.paragraph_format.line_spacing = 1.15
            if align is not None: p.alignment = align
        r = p.add_run(ln)
        set_run(r, size, bold, color, font=("Consolas" if mono else FONT))


CAP = 0
def add_table(headers, rows, caption=None, widths=None, body_size=9, mono_cols=()):
    global CAP
    if caption:
        CAP += 1
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
        set_run(p.add_run("表 %d  %s" % (CAP, caption)), 9.5, True, BROWN)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; shade(c, "E08A2E")
        cell_text(c, h, 9.5, True, WHITE, WD_ALIGN_PARAGRAPH.CENTER)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            c = cells[ci]
            if ri % 2 == 1: shade(c, "FCF3E4")
            cell_text(c, val, body_size, bold=(ci == 0),
                      color=(BROWN if ci == 0 else INK), mono=(ci in mono_cols))
    if widths:
        for r_ in t.rows:
            for i, w in enumerate(widths):
                r_.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '18')
    bt.set(qn('w:space'), '3'); bt.set(qn('w:color'), 'E08A2E')
    pbdr.append(bt); pPr.append(pbdr)
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'FCF3E4')
    pPr.append(sh)
    set_run(p.add_run(text), 15, True, BROWN)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
    lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '18')
    lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), 'B5600F')
    pbdr.append(lf); pPr.append(pbdr)
    set_run(p.add_run(text), 12.5, True, BROWN)


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    set_run(p.add_run(text), 10.5, True, RGBColor(0x44, 0x44, 0x44))


def body(text, size=10.5, color=INK, indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0.74) if indent else Cm(0)
    set_run(p.add_run(text), size, False, color)


def codeblock(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Cm(0.5)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
    lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '18')
    lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), 'E08A2E')
    pbdr.append(lf); pPr.append(pbdr)
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'F2F2F2')
    pPr.append(sh)
    for ln in text.strip("\n").split("\n"):
        r = p.add_run(ln)
        set_run(r, 9.5, ln.startswith("【"), BROWN if ln.startswith("【") else RGBColor(0x22, 0x33, 0x55), font="Consolas")
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.left_indent = Cm(0.5)
        pPr = p._p.get_or_add_pPr()
        sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'F2F2F2')
        pPr.append(sh)
    last = doc.paragraphs[-1]
    last._element.getparent().remove(last._element)


def callout(kind, title, text):
    conf = {'warn': ("FCF3E4", "E08A2E", BROWN),
            'tip':  ("EAF2FA", "1F4E79", RGBColor(0x1F, 0x4E, 0x79)),
            'note': ("F5F5F5", "9A9A9A", GRAY)}
    fill, bar, tc = conf[kind]
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Cm(0.3)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
    lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '24')
    lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), bar)
    pbdr.append(lf); pPr.append(pbdr)
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), fill)
    pPr.append(sh)
    r = p.add_run(title); set_run(r, 10, True, tc)
    for ln in text.split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.left_indent = Cm(0.3)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
        lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '24')
        lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), bar)
        pbdr.append(lf); pPr.append(pbdr)
        sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), fill)
        pPr.append(sh)
        set_run(p.add_run(ln), 9.5, False, INK)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def footer_page_number():
    p = doc.sections[0].footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(); set_run(r, 9, False, GRAY)
    for el, attr in (('w:fldChar', 'begin'), ('w:instrText', None), ('w:fldChar', 'end')):
        e = OxmlElement(el)
        if el == 'w:fldChar':
            e.set(qn('w:fldCharType'), attr)
        else:
            e.set(qn('xml:space'), 'preserve'); e.text = ' PAGE '
        r._r.append(e)


# ======================================================================
#              词表扁平化 + 检索式拼装（产品无关 · 模板已固化）
# ======================================================================
#
# 本区已固化为通用模板，换产品无需改动，只改上方 CONFIG 区。
#   · 每个库只输出一条「专业检索式」
#   · 万方用官方专业检索语法：全部:(词)，逻辑词小写 and / or
#   · PubMed / Embase 不加字段限定，便于直接粘进检索框
#   · 中文词自动「子串覆盖去重」，英文词自动「短语覆盖去重」
#
CJK = re.compile(r'[\u4e00-\u9fff]')


def need_quote(term):
    return not term.replace("_", "").isalnum()


def _q(term):
    return '"%s"' % term if need_quote(term) else term


def _flat_u2():
    out = []
    for m in MANUFACTURERS:
        n = max(len(m["en"]), len(m["cn"]))
        for i in range(n):
            if i < len(m["en"]): out.append(m["en"][i])
            if i < len(m["cn"]): out.append(m["cn"][i])
    return out


def _flat_u2_en():
    out = []
    for m in MANUFACTURERS:
        out.extend(m["en"])
    return out


DROPPED_LOG = []

# ★ 白名单：下列词即使被更短的同根词覆盖，也强制保留、不参与自动去重。
#   典型用法：NMPA 注册的官方通用名 / 说明书品名——宁可检索式略长，
#   也不能因为某个中文库采用分词检索（而非严格连续子串匹配）而漏检。
#   在上方 CONFIG 区写：KEEP_ALWAYS = ["某通用名"]；不写则为空。
try:
    KEEP_ALWAYS
except NameError:
    KEEP_ALWAYS = []


def dedup_cn(terms, unit=""):
    """中文子串覆盖去重：短词优先保留；已被保留词连续包含者，冗余删除。
    KEEP_ALWAYS 中的词一律保留。"""
    terms = list(dict.fromkeys(terms))
    keep, dropped = [], []
    order = {t: i for i, t in enumerate(terms)}
    for t in sorted(terms, key=len):
        if t in KEEP_ALWAYS:
            if t not in keep:
                keep.append(t)
            continue
        cov = next((k for k in keep if k != t and k in t), None)
        if cov:
            dropped.append((t, cov))
        else:
            keep.append(t)
    keep.sort(key=lambda x: order[x])
    for a, b in dropped:
        DROPPED_LOG.append((unit, a, "被「%s」覆盖，已删除" % b))
    return keep


def dedup_en(terms, unit=""):
    """英文短语覆盖去重：① 仅大小写不同者留一；
    ② 短语的组成词已被保留的单词覆盖 → 短语冗余；③ 短语被更短保留短语包含 → 冗余。
    KEEP_ALWAYS 中的词一律保留。"""
    terms = list(dict.fromkeys(terms))
    keep_s, dropped, seen = [], [], set()
    for t in terms:
        if " " in t:
            continue
        if t in KEEP_ALWAYS:
            if t not in keep_s:
                keep_s.append(t)
                seen.add(t.lower())
            continue
        if t.lower() in seen:
            dropped.append((t, "与已保留词仅大小写不同，已删除"))
            continue
        seen.add(t.lower())
        keep_s.append(t)
    slow = set(x.lower() for x in keep_s)
    phr = []
    for t in sorted([x for x in terms if " " in x], key=len):
        if t in KEEP_ALWAYS:
            if t not in phr:
                phr.append(t)
            continue
        ws = [w.lower().strip(",") for w in t.split()]
        if any(w in slow for w in ws):
            dropped.append((t, "其组成词已被保留的单词覆盖，已删除"))
            continue
        cov = next((k for k in phr if k in t), None)
        if cov:
            dropped.append((t, "被「%s」覆盖，已删除" % cov))
            continue
        phr.append(t)
    keep = list(dict.fromkeys([t for t in terms if t in keep_s or t in phr]))
    for a, b in dropped:
        DROPPED_LOG.append((unit, a, b))
    return keep


def dedup_cn_mixed(terms, unit=""):
    """中英混排词表：中文部分按连续子串去重，非中文词原样保留。
    ★ 语种归属由操作员填报的位置决定，不由字符决定——
      MANUFACTURERS["cn"] 里的 "BD" 这类拉丁缩写只进中文三库，不进英文库。"""
    terms = list(dict.fromkeys(terms))
    _k = set(dedup_cn([t for t in terms if CJK.search(t)], unit))
    _a = set(t for t in terms if not CJK.search(t))
    return [t for t in terms if t in _k or t in _a]





# ---- 单元词表（去重后）------------------------------------------------
CN_KEEP = dedup_cn_mixed([t for t, _ in CN_TERMS], "单元1")
BRAND_KEEP = dedup_en([t for t, _ in BRAND_TERMS], "单元1")
PREFIX_KEEP = dedup_en([t for t, _ in PREFIX_TERMS], "单元1")

U1_CN_LIB = CN_KEEP + BRAND_KEEP + [t for t in PREFIX_KEEP]
U1_EN_LIB = ([t for t in BRAND_KEEP if not CJK.search(t)]
             + [t for t in PREFIX_KEEP if not CJK.search(t)])

# ★ 中英先按语种拆开再各自去重：中文库(含英文词)与英文库用不同覆盖规则，
#   若在同一混合列表上跑中文子串规则，会出现跨语种误判
#   （例：厂家英文名尾部含 "BD" 会被中文组的 "BD" 误判为覆盖）与重复日志。
# ★ 语种归属按填报位置决定：declaredEnglish = MANUFACTURERS["en"]，其余一律只进中文三库
_U2_EN_RAW = _flat_u2_en()
_U2_MIX = _flat_u2()
U2_EN_LIB = dedup_en(_U2_EN_RAW, "单元2")
_U2_CN_PART = dedup_cn_mixed([t for t in _U2_MIX if t not in _U2_EN_RAW], "单元2")
U2_CN_LIB = list(dict.fromkeys(
    [t for t in _U2_MIX if t in U2_EN_LIB or t in _U2_CN_PART]))


# ---- 各库专业检索式（每库一条）----------------------------------------
def cnki_pro():
    """知网专业检索：FT = '词'，逻辑词 AND / OR"""
    a = " OR ".join("FT = '%s'" % t for t in U1_CN_LIB)
    b = " OR ".join("FT = '%s'" % t for t in U2_CN_LIB)
    return "(%s) AND (%s)" % (a, b)


def wanfang_pro():
    """万方专业检索：全部:(词)，逻辑词小写 and / or"""
    def v(t): return "全部:(%s)" % _q(t)
    a = " or ".join(v(t) for t in U1_CN_LIB)
    b = " or ".join(v(t) for t in U2_CN_LIB)
    return "(%s) and (%s)" % (a, b)


def vip_pro():
    """维普专业检索：U=词，逻辑词用 AND / OR（★ 不用 * / + 符号式）；含空格连字符的词加半角引号"""
    def v(t): return "U=%s" % _q(t.strip())
    a = " OR ".join(v(t) for t in U1_CN_LIB)
    b = " OR ".join(v(t) for t in U2_CN_LIB)
    return "(%s) AND (%s)" % (a, b)


def pubmed():
    """PubMed：不加字段限定，直接词 + AND / OR"""
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    return "(%s) AND (%s)" % (a, b)


def embase():
    """Embase：不加字段限定，默认检索全部字段"""
    def v(t):
        x = t.lower()
        if t in PREFIX_KEEP and len(t) >= 5:
            return "'%s*'" % x
        return "'%s'" % x if need_quote(x) else x
    a = " OR ".join(v(t) for t in U1_EN_LIB)
    b = " OR ".join(v(t) for t in U2_EN_LIB)
    return "(%s) AND (%s)" % (a, b)


def cochrane():
    """Cochrane Library：Search Manager 行号式"""
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    return "#1 (%s):ti,ab,kw\n#2 (%s):ti,ab,kw\n#3 #1 AND #2" % (a, b)


def ctgov():
    """ClinicalTrials.gov：Other terms 框"""
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    return "Other terms: (%s) AND (%s)" % (a, b)

# ======================================================================
#                              文档内容
# ======================================================================

for _ in range(2): doc.add_paragraph()
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run(PRODUCT_CN), 20, True, BROWN)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
set_run(p.add_run(SUBTITLE), 16, True, ORANGE)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(8)
set_run(p.add_run(SCOPE_NOTE), 11, False, GRAY)
doc.add_paragraph()

add_table(
    ["项目", "内容"],
    [
        ["检索单元", "① 产品 / 技术名（%d 词）　② 厂家名称（%d 词）"
         % (len(U1_CN_LIB), len(U2_CN_LIB))],
        ["检索逻辑", "单元① AND 单元②，各库一条专业检索式，一次出数"],
        ["检索字段", "知网 FT（全文）／万方 全部／维普 U（任意字段）／PubMed、Embase 不加字段限定"],
        ["语种范围", "中文三库检索中英文词；英文库只检索英文词，不检索中文词"],
        ["时间范围", "不限起始时间，建库至检索日"],
        ["输出", "各库命中数 → 决定是否进入二轮"],
    ],
    widths=[3.0, 12.8], body_size=9.5)

# ---- 一、检索词 ----
h1("一、检索词")

h2("1.1 单元 1　产品 / 技术名 / 商品名")
rows = []
for t, note in CN_TERMS:
    if t in CN_KEEP: rows.append(["中文", t, note, "仅中文三库"])
for t, note in BRAND_TERMS:
    if t in BRAND_KEEP: rows.append(["英文", t, note, "全部 7 库"])
for t, note in PREFIX_TERMS:
    if t in PREFIX_KEEP: rows.append(["英文", t, note, "中文三库加尾空格\n英文库不加"])
add_table(["语种", "检索词", "覆盖说明", "用于"], rows,
          widths=[1.2, 3.4, 9.8, 2.4], body_size=8.5, mono_cols=(1,),
          caption="单元 1 检索词（去重后：中文库 %d 词 / 英文库 %d 词，组内 OR）"
                  % (len(U1_CN_LIB), len(U1_EN_LIB)))

h2("1.2 单元 2　厂家名称中英文（含沿革）")
rows = []
for m in MANUFACTURERS:
    rows.append([m["period"], "\n".join(m["en"]), "\n".join(m["cn"]), m["note"]])
add_table(["时期", "英文", "中文", "说明"], rows,
          widths=[2.6, 4.0, 3.6, 5.6], body_size=8.5, mono_cols=(1, 2),
          caption="单元 2 检索词（原始填报 %d 词，去重后 %d 词，组内 OR）"
                  % (len(_flat_u2()), len(U2_CN_LIB)))

h2("1.3 ★ 子串覆盖去重记录")
body("检索词填报后自动执行覆盖去重：被更短词根覆盖的写法不再进入检索式，"
     "以避免检索式冗长并降低手工出错概率。全部被删词逐条记录如下，便于复核。", indent=False)
if DROPPED_LOG:
    add_table(["单元", "被删除的检索词", "原因"],
              [[u, a, b] for u, a, b in DROPPED_LOG],
              widths=[2.0, 6.2, 7.6], body_size=8.5, mono_cols=(1,),
              caption="被删检索词清单（共 %d 条）" % len(DROPPED_LOG))
callout("tip", "★ 去重规则",
        "中文库（知网 FT / 万方 全部 / 维普 U）按连续子串匹配：\n"
        "　若词 A 是词 B 的连续子串，则检索 A 即同时命中 B，B 冗余，自动删除。\n"
        "　前提是 A 具备唯一性——检索 A 不会卷入无关领域。若某词根过宽（会引入大量无关文献），\n"
        "　则它不能充当唯一词根，须改用修饰完整的写法，此时不要把它放进词表。\n"
        "英文库按词索引：\n"
        "　短语中任一词已被保留的单词覆盖（如已保留 Becton，则 Becton Dickinson 冗余），自动删除。\n"
        "　仅大小写不同的写法（如 PosiFlush / Posiflush）视为同一词，留一。")

# ---- 二、检索式 ----
h1("二、检索式（专业检索式，直接复制）")
body("每个库只给一条式子，均为该库的「专业检索」入口，可整体复制粘贴。", indent=False)

h2("2.1 中国知网 CNKI")
body("入口：知网首页 → 高级检索 → 专业检索。字段 FT = 全文，逻辑词用 AND / OR。", indent=False)
codeblock(cnki_pro())

h2("2.2 万方")
body("入口：万方首页 → 高级检索 → 专业检索。字段用「全部」，逻辑词用小写 and / or。", indent=False)
codeblock(wanfang_pro())

h2("2.3 维普")
body("入口：维普首页 → 高级检索 → 专业检索。运算符前后留空格；含连字符、空格的词须加半角双引号；"
     "不加引号为模糊检索、加引号为精确检索。", indent=False)
codeblock(vip_pro())

h2("2.4 PubMed")
body("直接粘贴到 PubMed 检索框，不加字段限定。含空格的词组已自动加引号，单词直接检索。", indent=False)
codeblock(pubmed())

h2("2.5 Embase")
body("直接粘贴到 Embase 检索框，默认检索全部字段。", indent=False)
codeblock(embase())

h2("2.6 Cochrane Library（CDSR + CENTRAL）")
body("Search Manager 行号式，逐行输入后由 #3 组合。", indent=False)
codeblock(cochrane())

h2("2.7 ClinicalTrials.gov")
body("粘贴到 Other terms 检索框。", indent=False)
codeblock(ctgov())

# ---- 三、命中数记录 ----
h1("三、命中数记录表（执行后填写）")
h2("3.1 英文数据库")
add_table(["数据库", "一轮命中数", "检索日期", "备注（异常记录）"],
          [["PubMed", "", "", ""], ["Embase", "", "", ""],
           ["Cochrane CDSR", "", "", ""], ["Cochrane CENTRAL", "", "", ""],
           ["ClinicalTrials.gov", "", "", ""]],
          widths=[3.8, 3.0, 3.0, 6.0])
h2("3.2 中文数据库")
add_table(["数据库", "一轮命中数", "检索日期", "备注（异常记录）"],
          [["中国知网 CNKI", "", "", ""], ["万方", "", "", ""], ["维普", "", "", ""]],
          widths=[3.8, 3.0, 3.0, 6.0])

# ---- 四、判定 ----
h1("四、一轮判定与下一步")
add_table(
    ["单库命中数", "判读", "下一步动作"],
    [
        ["0 条", "过严，或该库不收录此类文献",
         "拆开单跑：先只跑单元 1，再只跑单元 2。\n"
         "单元 1 有量而交集为 0 → 厂家 AND 过严，厂家词退出 AND 层，改放 OR 层"],
        ["1–20 条", "偏少，可能遗漏",
         "放宽：删去厂家 AND 段；\n或回头补品牌拼写变体、补厂家历史名称"],
        ["20–300 条", "★ 召回健康，可作核心盘子", "定稿为终版检索式，进入查全验证"],
        ["> 300 条", "过宽，噪声大",
         "进入二轮：在末尾 AND 叠加使用部位 / 适应证词，字段仍用全文、不切字段"],
    ],
    widths=[2.6, 4.6, 8.6])

h2("加严阶梯（增加限定词，字段不变）")
add_table(
    ["顺序", "手段", "是否安全", "说明"],
    [
        ["A", "AND 使用部位 / 适应证词", "★ 优先、无损",
         "部位词取自申报产品说明书【适用范围 / 适应证】章节，"
         "以及说明书引用文献的实际应用场景。必须用本产品自己的适用范围，不得套用他产品"],
        ["A′", "删去部位组中最宽的词，只留窄词", "仍属 A 类，先于 B 试尽",
         "例：删去最宽的解剖部位统称，只保留具体病种 / 使用场景词"],
        ["B1", "中文产品名逐级收窄", "有损", "把宽的中文词组换为更长的中文词组"],
        ["B2", "品牌词根 → 官方完整产品名", "有损", "把品牌词根换为注册证 / 510(k) 的官方完整产品名"],
        ["B3", "AND 技术特指词", "有损", "追加一段产品技术特征词 AND"],
        ["B4", "AND 术式 / 路径词", "有损", "追加一段术式或入路词 AND"],
    ],
    widths=[1.4, 4.2, 3.0, 7.2], body_size=9)
callout("warn", "⚠ 三条铁律（贯穿全程）",
        "1）只在末尾 AND 叠加新单元，绝不删改已有单元——命中集单调收窄，各轮结果才可对拍。\n"
        "2）字段始终用全文，不切题摘降噪——收敛靠加限定词，不靠切字段。\n"
        "3）禁用 NOT 排除词，一律靠加限定词收敛。")

# ---- 五、查全验证 ----
h1("五、定稿前必做：查全验证")
body("命中数合理不等于没有漏检。取说明书或已知文献引用的金标准文献，在终版检索式中逐条回检，"
     "任一条未被召回即说明词表存在缺口，须补词后全库重跑。", indent=False)
add_table(["金标准文献", "来源", "是否被终版召回"],
          [[g, GOLD_SRC, "□ 是　□ 否"] for g in GOLD_REFS],
          widths=[7.6, 4.6, 3.6], body_size=9,
          caption="查全验证基线文献")
callout("tip", "★ 验证怎么做",
        "把每篇金标准文献的题名逐条粘进终版检索式所在的库，确认每一篇都能被召回。\n"
        "若有文献未被召回，记录它使用的产品名称 / 厂家写法 / 用途写法，"
        "以 OR 补入词表后全库重跑，并在筛选报告中写明补词依据与来源。")

footer_page_number()

out = OUT
base, ext = os.path.splitext(OUT)
i = 1
while os.path.exists(out):
    out = "%s_%d%s" % (base, i, ext); i += 1
doc.save(out)
print("SAVED:", out)
