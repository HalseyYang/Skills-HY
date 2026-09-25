# -*- coding: utf-8 -*-
"""
【第 5 轮】检索词与检索式文档生成器（产品无关骨架 · 模板）
==========================================================
skill：文献检索词与检索式生成skill

一轮 = 单元1(产品/技术名) AND 单元2(厂家名)
二轮 = 单元1 AND 单元2 AND 单元3(使用部位)
三轮 = 单元1 AND 单元2 AND 单元3 AND 单元4(精确产品名)      ← 单元4 为本轮新增

单元1/2/3 一字不改、字段一点不切，只在末尾 AND 叠加单元4，
故三轮命中集 ⊆ 二轮 ⊆ 一轮，三轮结果全部可对拍。

前置条件：二轮（含 A′ 部位词收窄）跑完仍过宽，
且已做干扰源归因、确认干扰来自同厂家其他产品，并已逐张核实注册证 product name。
单元 1/2/3 的 CONFIG 段直接从 gen_round2_doc.py **原样复制**，一字不改。

★ 注意：单元 4 与单元 1 共用品牌词时，「库内二次检索」校验会失灵，
  本轮必须补做「取交集」校验，详见 SKILL.md 第 5.4 节。
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

OUT = r"C:/Users/lenovo/Desktop/三轮检索_workbuddy版本.docx"

PRODUCT_CN = "（产品中文名）"
SUBTITLE   = "三轮检索词与检索式（精确产品名·加严版）"
SCOPE_NOTE = "在二轮「产品名 AND 厂家名 AND 使用部位」基础上，AND 叠加单元 4（精确产品名）"

R2_DOC = "《（二轮检索文档名）》"

# ---- 单元 1：产品 / 技术名（★ 与一轮完全一致，不要改动）--------------
CN_TERM      = "（中文通用词）"
CN_TERM_NOTE = "一个词覆盖该类产品全部中文写法"
CN_TERMS     = [(CN_TERM, CN_TERM_NOTE)]

# ★ KEEP_ALWAYS：子串覆盖去重的白名单。凡「能在注册证 / 指导原则 / 已发表文献里
#   指认出来源」的产品名一律写进来（官方通用名、CMDE 品名举例、同类注册名、实证异写）。
#   原因：自动去重按连续子串删词，而部分中文库（知网 FT）按分词命中，
#   删掉这些名会整批漏检——召回损失远大于检索式多几个词的代价。
#   例：KEEP_ALWAYS = ["口腔修复膜", "可吸收口腔修复膜", "口腔可吸收修复膜"]
KEEP_ALWAYS = []

BRAND_TERMS  = [
    ("（品牌词根）",   "★ 覆盖全部带该词根的产品英文全名，故不再单列全名"),
    ("（空格写法）",   "空格写法"),
    ("（连写写法）",   "合并连写写法"),
    ("（技术特征词）", "技术文献中的通用写法（不依赖品牌名）"),
]
PREFIX_TERMS = [
    ("（技术词）", "★ 前缀匹配，一条覆盖全部派生词组"),
    ("（缩写）",   "★ 前缀匹配，注意缩写歧义"),
]

# ---- 单元 2：厂家名称（★ 与一轮完全一致，不要改动）-------------------
MANUFACTURERS = [
    {"period": "（时期1）", "en": ["（英文实体名）", "（英文子品牌）"],
     "cn": ["（中文译名1）", "（中文译名2）"], "note": "（沿革说明）"},
    {"period": "（时期2）", "en": ["（英文实体名）"], "cn": ["（中文译名）"],
     "note": "（沿革说明）"},
    {"period": "（时期3·现名）", "en": ["（英文现名）"], "cn": ["（中文现名）"],
     "note": "（沿革说明）"},
]

# ---- 单元 3：使用部位（★ 与二轮完全一致，不要改动）-------------------
SITE_CN = {
    "（部位组1）": [
        ("（中文部位词·最宽）", "最宽部位词，覆盖无法穷举的写法"),
        ("（中文疾病词1）",     "该部位疾病统称"),
        ("（中文疾病词2）",     "具体病理类型；宽词不含此串，须单列"),
    ],
    "（部位组2）": [
        ("（中文部位词）", "该部位肿瘤统称"),
        ("（中文疾病词）", "具体病种；★ 经典适应证，须单列"),
    ],
}
SITE_EN = {
    "（部位组1）": [
        ("（site word 1）", "含该词即命中，词组写法无需单列"),
        ("（site word 2）", "形容词形式，词根不同，须单列"),
    ],
    "（部位组2）": [
        ("（site word 1）", "含该词即命中"),
        ("（site phrase）", "★ 经典适应证，不含宽词词根，必须单列"),
    ],
}
SITE_ORDER = ["（部位组1）", "（部位组2）"]
CNDB_USE_EN_SITE = True

# ---- 单元 4：精确产品名（★ 三轮唯一新增项）---------------------------
# 取词来源：英文取 FDA 510(k) 的 device_name 字段（openFDA API 可查）；
#           中文取 NMPA 注册证的产品名称。
# 备注栏**必须标注覆盖关系**——品牌词根是否已覆盖该官方名，避免误判加严有效。
# 含中文的词会自动只在中文三库出现，英文库自动剔除。
SPEC_TERMS = [
    ("（品牌词根）", "★ 品牌词根。英文库按词索引，本词已覆盖下列全部官方完整产品名"),
    ("（空格写法）", "空格写法"),
    ("（连写写法）", "合并连写写法"),
    ("（品牌特有的非常规写法）",
     "★ 文献中出现的非常规写法（如 brand + 配件名词组），不被品牌词根覆盖，须单列"),
    ("（FDA 官方产品名1）", "FDA 官方产品名（Kxxxxxx，申请人 XXX）——被品牌词根覆盖"),
    ("（FDA 官方产品名2）", "FDA 官方产品名（Kxxxxxx，申请人 XXX）——被品牌词根覆盖"),
    ("（本地语言官方注册名）",
     "★ NMPA 官方中文产品名（注册证号略）。纯本地写法，"
     "与英文品牌无覆盖关系，是本组唯一有召回增量的词"),
]

# ---- 备选词（本轮排除，三轮过窄时按需追加）---------------------------
# 每项是 (备选词, 说明, 排除影响)。排除影响要写清「会漏掉哪类文献」。
SPEC_OPTIONAL = [
    ("（英文技术特指词）", "捞「不写品牌只写技术」的国外文献", "本轮排除；排除后此类文献会漏检"),
    ("（本地语言技术特指词）", "★ 本地文献最常见写法（附实证出处）", "本轮排除；本轮最大的漏检来源，过窄时优先追加"),
    ("（词序变体）", "本地语言不做词序归一化", "本轮排除"),
]

# ---- 干扰源排查（同厂家旗下其他同类产品）-----------------------------
# 每项是 (产品, 用途, 干扰程度, 说明与处理)。
# ★ 这一步必须在加严前做——先归因，再决定加什么。
INTERFERERS = [
    ("（目标产品）", "（用途）", "—", "目标产品"),
    ("（同厂家其他产品1）", "（用途）", "★★★ 最主要",
     "注册证号 xxx；属同集团。二轮某部位词组会精准命中其文献。"
     "三轮加单元 4 后应被排除，但同一篇文献若同时提及两款产品仍会命中，需人工判读"),
    ("（其他能量平台产品）", "（用途）", "★★",
     "单元 1 无该技术词，但对比研究常同时出现通用技术词与厂家名，会被捞入"),
]

# ---- 本轮决策记录（写入文档「零」章，便于追溯）-----------------------
DECISIONS = [
    ("申报产品", "（产品名称）", "用户确认。对应注册证 xxx；适用范围为 xxx"),
    ("单元 4 力度", "仅品牌变体 + 官方完整产品名", "用户确认。被排除的词进备选词表，过窄时按需追加"),
    ("单元 3 部位词", "保留（部位组1）+（部位组2）", "用户确认"),
    ("单元 1 / 2 / 3 是否改动", "全部沿用，一字不改", "只在末尾 AND 叠加单元 4，保证三轮 ⊆ 二轮 ⊆ 一轮"),
    ("单元 1 通用技术词是否删除", "保留", "单元 4 已锁定品牌，宽词逻辑上不再贡献召回；"
     "但保留可维持词表一致、子集对拍成立，且单元 4 放宽时可复用"),
]

# ---- 开口项 ----------------------------------------------------------
OPEN_ITEMS = [
    ("（开口项1）", "（说明与影响）"),
    ("（开口项2）", "（说明与影响）"),
]

# ======================================================================
#                          以下为生成逻辑
# ======================================================================

ORANGE = RGBColor(0xE0, 0x8A, 0x2E); BROWN  = RGBColor(0xB5, 0x60, 0x0F)
CREAM  = RGBColor(0xFC, 0xF3, 0xE4); INK    = RGBColor(0x33, 0x33, 0x33)
GRAY   = RGBColor(0x5A, 0x5A, 0x5A); WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
RED    = RGBColor(0xA3, 0x2D, 0x2D)
FONT   = "微软雅黑"

CJK = re.compile(r'[\u4e00-\u9fff]')

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


def bd_shd(fill="FCF3E4"):
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), fill)
    return sh


def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '18')
    bt.set(qn('w:space'), '3'); bt.set(qn('w:color'), 'E08A2E')
    pbdr.append(bt); pPr.append(bd_shd())
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
    pPr.append(bd_shd("F2F2F2"))
    for ln in text.strip("\n").split("\n"):
        r = p.add_run(ln)
        set_run(r, 9.5, ln.startswith("【"), BROWN if ln.startswith("【") else RGBColor(0x22, 0x33, 0x55), font="Consolas")
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0); p.paragraph_format.left_indent = Cm(0.5)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
        lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '18')
        lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), 'E08A2E')
        pbdr.append(lf); pPr.append(pbdr)
        pPr.append(bd_shd("F2F2F2"))
    last = doc.paragraphs[-1]
    last._element.getparent().remove(last._element)


def callout(kind, title, text):
    conf = {'warn': ("FCF3E4", "E08A2E", BROWN),
            'tip':  ("EAF2FA", "1F4E79", RGBColor(0x1F, 0x4E, 0x79)),
            'note': ("F5F5F5", "9A9A9A", GRAY),
            'ok':   ("EAF6EC", "2E7D32", RGBColor(0x2E, 0x7D, 0x32)),
            'err':  ("FCEBEB", "A32D2D", RED)}
    fill, bar, tc = conf[kind]
    def mkp(first=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6) if first else Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.left_indent = Cm(0.3)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement('w:pBdr'); lf = OxmlElement('w:left')
        lf.set(qn('w:val'), 'single'); lf.set(qn('w:sz'), '24')
        lf.set(qn('w:space'), '6'); lf.set(qn('w:color'), bar)
        pbdr.append(lf); pPr.append(pbdr)
        pPr.append(bd_shd(fill))
        return p
    p = mkp(True)
    set_run(p.add_run(title), 10, True, tc)
    for ln in text.split("\n"):
        p = mkp()
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

SITE_CN_KEEP, SITE_EN_KEEP = {}, {}
for _g in SITE_ORDER:
    SITE_CN_KEEP[_g] = dedup_cn_mixed([t for t, _ in SITE_CN[_g]], "单元3")
    SITE_EN_KEEP[_g] = dedup_en([t for t, _ in SITE_EN[_g]], "单元3")

_spec_cn = [t for t, _ in SPEC_TERMS if CJK.search(t)]
_spec_en = [t for t, _ in SPEC_TERMS if not CJK.search(t)]
U4_CN_KEEP = dedup_cn(_spec_cn, "单元4")
U4_EN_KEEP = dedup_en(_spec_en, "单元4")
U4_CN_LIB = U4_EN_KEEP + U4_CN_KEEP
U4_EN_LIB = U4_EN_KEEP

G_ALL = list(SITE_ORDER)


def site_cn(groups):
    out = []
    for g in groups:
        out += SITE_CN_KEEP[g]
        if CNDB_USE_EN_SITE:
            out += SITE_EN_KEEP[g]
    return out


def site_en(groups):
    out = []
    for g in groups:
        out += SITE_EN_KEEP[g]
    return out


# ---- 各库专业检索式 ---------------------------------------------------
def cnki_pro(groups):
    a = " OR ".join("FT = '%s'" % t for t in U1_CN_LIB)
    b = " OR ".join("FT = '%s'" % t for t in U2_CN_LIB)
    c = " OR ".join("FT = '%s'" % t for t in site_cn(groups))
    d = " OR ".join("FT = '%s'" % t for t in U4_CN_LIB)
    return "(%s) AND (%s) AND (%s) AND (%s)" % (a, b, c, d)


def wanfang_pro(groups):
    def v(t): return "全部:(%s)" % _q(t)
    a = " or ".join(v(t) for t in U1_CN_LIB)
    b = " or ".join(v(t) for t in U2_CN_LIB)
    c = " or ".join(v(t) for t in site_cn(groups))
    d = " or ".join(v(t) for t in U4_CN_LIB)
    return "(%s) and (%s) and (%s) and (%s)" % (a, b, c, d)


def vip_pro(groups):
    def v(t): return "U=%s" % _q(t.strip())
    a = " OR ".join(v(t) for t in U1_CN_LIB)
    b = " OR ".join(v(t) for t in U2_CN_LIB)
    c = " OR ".join(v(t) for t in site_cn(groups))
    d = " OR ".join(v(t) for t in U4_CN_LIB)
    return "(%s) AND (%s) AND (%s) AND (%s)" % (a, b, c, d)


def pubmed(groups):
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    c = " OR ".join(_q(t) for t in site_en(groups))
    d = " OR ".join(_q(t) for t in U4_EN_LIB)
    return "(%s) AND (%s) AND (%s) AND (%s)" % (a, b, c, d)


def embase(groups):
    def v(t):
        x = t.lower()
        if t in PREFIX_KEEP and len(t) >= 5:
            return "'%s*'" % x
        return "'%s'" % x if need_quote(x) else x
    a = " OR ".join(v(t) for t in U1_EN_LIB)
    b = " OR ".join(v(t) for t in U2_EN_LIB)
    c = " OR ".join(v(t) for t in site_en(groups))
    d = " OR ".join(v(t) for t in U4_EN_LIB)
    return "(%s) AND (%s) AND (%s) AND (%s)" % (a, b, c, d)


def cochrane(groups):
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    c = " OR ".join(_q(t) for t in site_en(groups))
    d = " OR ".join(_q(t) for t in U4_EN_LIB)
    return ("#1 (%s):ti,ab,kw\n#2 (%s):ti,ab,kw\n#3 (%s):ti,ab,kw\n#4 (%s):ti,ab,kw\n"
            "#5 #1 AND #2 AND #3 AND #4" % (a, b, c, d))


def ctgov(groups):
    a = " OR ".join(_q(t) for t in U1_EN_LIB)
    b = " OR ".join(_q(t) for t in U2_EN_LIB)
    c = " OR ".join(_q(t) for t in site_en(groups))
    d = " OR ".join(_q(t) for t in U4_EN_LIB)
    return "Other terms: (%s) AND (%s) AND (%s) AND (%s)" % (a, b, c, d)

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
        ["检索单元", "① 产品 / 技术名（%d 词）　② 厂家名称（%d 词）\n"
                     "③ 使用部位 / 适应证（全量 %d 词）　④ 精确产品名（%d 词）"
         % (len(U1_CN_LIB), len(U2_CN_LIB), len(site_cn(G_ALL)), len(U4_CN_LIB))],
        ["检索逻辑", "单元① AND ② AND ③ AND ④，各库一条专业检索式"],
        ["检索字段", "与前两轮完全一致（知网 FT／万方 全部／维普 U／PubMed、Embase 不加字段）"],
        ["与二轮的关系", "单元①②③原样沿用，仅在末尾 AND 叠加单元④；三轮命中集必为二轮子集"],
        ["语种范围", "中文三库检索中英文词；英文库只检索英文词，不检索中文词"],
        ["输出", "各库三轮命中数 + 分部位命中数 → 三级收敛率 → 定稿判定"],
    ],
    widths=[3.0, 12.8], body_size=9.5)

# ---- 零、决策记录 ----
h1("零、本轮决策记录")
add_table(["决策项", "结论", "依据"], [[a, b, c] for a, b, c in DECISIONS],
          widths=[3.6, 5.4, 6.8], body_size=9)

# ---- 一、产品核实与干扰源 ----
h1("一、产品核实与干扰源排查（加严前必做）")
body("命中量大不等于词不够严。加严前必须先回答「多出来的是谁」——"
     "先做干扰源归因，再决定加什么。本节需逐张核实注册证的产品名称（product name），"
     "不能只看厂家名与适用范围。", indent=False)
add_table(["产品 / 干扰源", "用途", "干扰程度", "说明与处理"],
          [[a, b, c, d] for a, b, c, d in INTERFERERS],
          widths=[3.4, 3.0, 1.8, 7.6], body_size=8.5)

# ---- 二、变化对照 ----
h1("二、三轮相对二轮的变化")
add_table(
    ["检索要素", "一轮", "二轮", "三轮", "变化说明"],
    [
        ["单元 1　产品 / 技术名", "%d 词" % len(U1_CN_LIB), "%d 词" % len(U1_CN_LIB),
         "%d 词" % len(U1_CN_LIB), "原样沿用，一字不改"],
        ["单元 2　厂家名称", "%d 词" % len(U2_CN_LIB), "%d 词" % len(U2_CN_LIB),
         "%d 词" % len(U2_CN_LIB), "原样沿用，一字不改"],
        ["单元 3　使用部位", "无", "%d 词" % len(site_cn(G_ALL)),
         "%d 词" % len(site_cn(G_ALL)), "原样沿用，一字不改"],
        ["单元 4　精确产品名", "无", "无", "新增 %d 词" % len(U4_CN_LIB),
         "★ 本轮唯一新增项，以 AND 叠加"],
        ["检索字段", "全文", "全文", "全文", "★ 全程不切字段"],
    ],
    widths=[3.0, 1.9, 1.9, 2.1, 6.9], body_size=8.5)

h2("2.1 单元 4　精确产品名（新增）")
body("取词来源：英文取 FDA 510(k) 的 device_name 字段，中文取 NMPA 注册证的产品名称。"
     "备注栏逐条标注覆盖关系——品牌词根是否已覆盖该官方名，避免误判加严有效。", indent=False)
rows = []
for t, n in SPEC_TERMS:
    if t in U4_EN_KEEP or t in U4_CN_KEEP:
        rows.append(["中文" if CJK.search(t) else "英文", t, n])
add_table(["语种", "检索词", "覆盖关系说明"], rows,
          widths=[1.2, 4.6, 10.0], body_size=8.5, mono_cols=(1,),
          caption="单元 4 检索词（去重后：中文库 %d 词 / 英文库 %d 词）"
                  % (len(U4_CN_LIB), len(U4_EN_LIB)))

h2("2.2 备选词表（本轮排除，过窄时按序追加）")
add_table(["备选词", "捞什么", "排除影响"], [[a, b, c] for a, b, c in SPEC_OPTIONAL],
          widths=[3.4, 6.4, 6.0], body_size=8.5, mono_cols=(0,))

h2("2.3 ★ 子串覆盖去重记录")
if DROPPED_LOG:
    add_table(["单元", "被删除的检索词", "原因"],
              [[u, a, b] for u, a, b in DROPPED_LOG],
              widths=[2.0, 6.2, 7.6], body_size=8.5, mono_cols=(1,),
              caption="被删检索词清单（共 %d 条）" % len(DROPPED_LOG))
callout("tip", "★ 去重规则",
        "中文库按连续子串匹配：若词 A 是词 B 的连续子串，检索 A 即命中 B，B 冗余，自动删除。\n"
        "　前提是 A 具备唯一性（检索 A 不卷入无关领域）；过宽的词根不能充当唯一词根。\n"
        "英文库按词索引：短语中任一词已被保留的单词覆盖，该短语即冗余，自动删除。")

# ---- 三、检索式 ----
h1("三、检索式（专业检索式，直接复制）")
body("每个库给 %d 组式子：① 全量（%s）② 各组分部位式。"
     % (1 + len(SITE_ORDER), " ∪ ".join(SITE_ORDER)), indent=False)

h2("3.1 中国知网 CNKI")
body("入口：知网首页 → 高级检索 → 专业检索。字段 FT = 全文，逻辑词用 AND / OR。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(cnki_pro(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(cnki_pro([g]))

h2("3.2 万方")
body("入口：万方首页 → 高级检索 → 专业检索。字段用「全部」，逻辑词用小写 and / or。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(wanfang_pro(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(wanfang_pro([g]))

h2("3.3 维普")
body("入口：维普首页 → 高级检索 → 专业检索。运算符前后留空格；含连字符、空格的词须加半角双引号。",
     indent=False)
codeblock("【三轮 · 全量】"); codeblock(vip_pro(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(vip_pro([g]))

h2("3.4 PubMed")
body("直接粘贴到检索框，不加字段限定。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(pubmed(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(pubmed([g]))

h2("3.5 Embase")
body("直接粘贴到检索框，默认检索全部字段。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(embase(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(embase([g]))

h2("3.6 Cochrane Library（CDSR + CENTRAL）")
body("Search Manager 行号式，逐行输入。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(cochrane(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(cochrane([g]))

h2("3.7 ClinicalTrials.gov")
body("粘贴到 Other terms 检索框。", indent=False)
codeblock("【三轮 · 全量】"); codeblock(ctgov(G_ALL))
for g in SITE_ORDER:
    codeblock("【三轮 · %s】" % g); codeblock(ctgov([g]))

# ---- 四、命中数 ----
h1("四、命中数记录与三级收敛核算（执行后填写）")
_hdr = (["数据库", "一轮", "二轮全量"]
        + ["二轮·%s" % g for g in SITE_ORDER]
        + ["三轮全量", "收敛率", "检索日期"])
_w = [2.6, 1.4, 1.6] + [1.6] * len(SITE_ORDER) + [1.6, 1.6, 1.8]
_blank = lambda n: [n] + [""] * (len(_hdr) - 1)
h2("4.1 英文数据库")
add_table(_hdr, [_blank("PubMed"), _blank("Embase"), _blank("Cochrane CDSR"),
                 _blank("Cochrane CENTRAL"), _blank("ClinicalTrials.gov")],
          widths=_w, body_size=8)
h2("4.2 中文数据库")
add_table(_hdr, [_blank("中国知网 CNKI"), _blank("万方"), _blank("维普")],
          widths=_w, body_size=8)
body("收敛率 = 三轮全量 ÷ 一轮命中。三级命中数须一并写入筛选报告，"
     "形成完整的收敛证据链：一轮 → 二轮全量 → 二轮分部位 → 三轮全量。", indent=False)

# ---- 五、子集校验 ----
h1("五、子集校验（三轮 ⊆ 二轮 ⊆ 一轮，必做）")
add_table(
    ["方法", "操作", "判读标准"],
    [
        ["A　库内二次检索", "在已跑完的三轮结果集内，再用二轮式检索一次",
         "结果数应等于三轮数。★ 本轮单元 4 与单元 1 共用品牌词，该方法鉴别力下降"],
        ["B　取交集（★ 本轮必做）",
         "分别导出二轮、三轮题录，按题名 / DOI 取交集",
         "交集数应等于三轮数；单元 4 与单元 1 词重叠时，只有此方法能兜住改动"],
        ["C　抽样回检", "随机抽 10 篇三轮命中文献，用二轮式逐条回检", "10 篇应全部被二轮式命中"],
    ],
    widths=[3.4, 6.4, 6.0], body_size=9)
callout("warn", "⚠ 为什么本轮必须补做「取交集」",
        "单元 4 与单元 1 共用同一批品牌词，若检索式被误改、而改动恰好落在重叠词上，\n"
        "「库内二次检索」发现不了——它没有鉴别力。必须用题录级别的取交集比对兜住这个盲区。")

# ---- 六、判定 ----
h1("六、三轮后判断与下一步")
add_table(
    ["三轮单库命中数", "判读", "下一步"],
    [
        ["0 条", "单元 4 过严，或产品名写法有遗漏",
         "逐词单跑单元 4，看哪个词有量；检查品牌拼写变体是否收全（连字符 / 空格 / 连写）"],
        ["1–20 条", "偏少",
         "从备选词表按序追加技术特指词；或去掉单元 4，回到二轮式"],
        ["20–300 条", "★ 召回健康", "定稿为终版检索式，进入查全验证"],
        ["> 300 条", "已到收敛终点",
         "三选一：① 部位词收窄（删最宽统称词）；② 单元 2 只留产品实际上市主体；"
         "③ 接受命中量，在初筛阶段人工判读并写明排除理由"],
    ],
    widths=[2.8, 4.4, 8.6], body_size=9)
callout("note", "★ 单元 4 能排除什么、不能排除什么",
        "能排除：同厂家其他产品**未提及本产品品牌**的文献。\n"
        "不能排除：**同一篇文献同时提及两款产品**（对比研究、产品线综述）——"
        "这类只能靠初筛人工判读，判读依据应写进筛选报告的排除理由表。")

h2("定稿前必做：查全验证")
body("取说明书或已知同品种文献引用的金标准文献，在终版检索式中逐条回检，"
     "任一条未被召回即说明词表存在缺口，须补词后全库重跑。", indent=False)
add_table(["金标准文献", "来源", "是否被终版召回"],
          [["（待回填 1）", R2_DOC + "／说明书", "□ 是　□ 否"],
           ["（待回填 2）", R2_DOC + "／说明书", "□ 是　□ 否"],
           ["（待回填 3）", R2_DOC + "／说明书", "□ 是　□ 否"]],
          widths=[8.0, 4.8, 3.0], body_size=9, caption="查全验证基线文献（待回填）")

# ---- 七、开口项 ----
h1("七、开口项（需在定稿前闭合）")
add_table(["开口项", "说明与影响"], [[a, b] for a, b in OPEN_ITEMS],
          widths=[4.2, 11.6], body_size=9)

footer_page_number()

out = OUT
base, ext = os.path.splitext(OUT)
i = 1
while os.path.exists(out):
    out = "%s_%d%s" % (base, i, ext); i += 1
doc.save(out)
print("SAVED:", out)
