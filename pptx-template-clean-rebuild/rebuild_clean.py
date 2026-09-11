# -*- coding: utf-8 -*-
"""干净重建 pptx 包：修正 presentation.xml.rels 中的重复/悬空 slide 引用
（模板孤儿 rId3 与 python-pptx 新引用同时指向 slide1.xml），重建 sldIdLst。
只删孤儿 tag parts，绝不误删 slide / master / layouts / theme / media。"""
import zipfile, os, re

SRC = "clinical_evaluation_lecture_01.pptx"
TMP = "clinical_evaluation_lecture_01_rebuild.pptx"

with zipfile.ZipFile(SRC, "r") as zin:
    names = zin.namelist()
    data = {n: zin.read(n) for n in names}

pres = data["ppt/presentation.xml"].decode("utf-8")
rels = data["ppt/_rels/presentation.xml.rels"].decode("utf-8")

# sldIdLst 顺序（决定页面顺序）
sld_ids = re.findall(r'<p:sldId\s+id="(\d+)"\s+r:id="(rId\d+)"\s*/>', pres)
print("sldIdLst 条目数:", len(sld_ids))

# rels 中所有 Relationship
relationships = []
for m in re.finditer(r'<Relationship\b[^>]*/>', rels):
    tag = m.group(0)
    rId = re.search(r'Id="([^"]+)"', tag).group(1)
    typ = re.search(r'Type="([^"]+)"', tag).group(1)
    tgt = re.search(r'Target="([^"]+)"', tag).group(1)
    relationships.append((rId, typ, tgt))
rel_by_rId = {rId: (typ, tgt) for rId, typ, tgt in relationships}
print("rels 关系数:", len(relationships))

# 页面顺序对应的 slide 文件（rel 目标形式，如 slides/slide1.xml）
ordered_targets = [rel_by_rId[rid][1] for _id, rid in sld_ids]
print("页面顺序:", ordered_targets[:3], "..." , ordered_targets[-2:])

# ===== 非 slide 关系保留原名 =====
non_slide = [(rId, typ, tgt) for rId, typ, tgt in relationships if not typ.endswith("/slide")]
slide_old_rIds = [rid for _id, rid in sld_ids]

# ===== 分配新 slide rId（保持 rId11..rId39 不变亦可，但重排保证连续且不与 orphan 冲突）=====
new_parts = []
for rId, typ, tgt in non_slide:
    new_parts.append(f'<Relationship Id="{rId}" Type="{typ}" Target="{tgt}"/>')

# 给 slide 分配新 rId：从「非 slide 关系的最大数字 Id + 1」开始，连续。
# 关键：不能硬编码从 11 开始——非 slide 关系（notesMaster/handoutMaster/
# presProps/viewProps/tableStyles/commentAuthors/tags）常占用 rId32..rId38，
# 若 slide 硬编号 rId11..rId39 会从第 22 页起撞号 → 22-28 页黑屏/空白。
def _rid_num(rid):
    return int(re.sub(r'\D', '', rid) or "0")
start = max((_rid_num(rid) for rid, _, _ in non_slide), default=0) + 1
new_slide_rId = {}
for i, old_rid in enumerate(slide_old_rIds):
    r = f"rId{start+i}"
    new_slide_rId[old_rid] = r
    tgt = rel_by_rId[old_rid][1]
    new_parts.append(
        f'<Relationship Id="{r}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="{tgt}"/>')

new_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(new_parts) + "</Relationships>")
data["ppt/_rels/presentation.xml.rels"] = new_rels.encode("utf-8")
print("重写 presentation.xml.rels，slide 只剩连续唯一引用")

# 重建 sldIdLst
new_ids = ""
for i, (_oid, old_rid) in enumerate(sld_ids):
    new_ids += f'<p:sldId id="{256+i}" r:id="{new_slide_rId[old_rid]}"/>'
new_lst = '<p:sldIdLst>' + new_ids + '</p:sldIdLst>'
data["ppt/presentation.xml"] = re.sub(
    r'<p:sldIdLst>.*?</p:sldIdLst>', new_lst, pres, flags=re.DOTALL).encode("utf-8")
print("重写 sldIdLst")

# ===== 删除孤儿 tag parts（无引用关系引用的 tag）=====
# 收集全部被引用的 target（完整路径）
referenced = set()
for rId, typ, tgt in relationships:
    if tgt.startswith("/"):
        referenced.add(tgt.lstrip("/"))
    elif tgt.startswith("../"):
        referenced.add(tgt.split("../",1)[1])  # 保守，但 tag 通常直接引用
    else:
        # 相对 ppt/ 的 target，转完整路径；若是 slides/slide1.xml 这种
        if tgt.startswith("slides/"):
            referenced.add("ppt/" + tgt)
        elif tgt.startswith("theme/"):
            referenced.add("ppt/" + tgt)
        elif tgt.startswith("slideMasters/"):
            referenced.add("ppt/" + tgt)
        elif tgt.startswith("slideLayouts/"):
            referenced.add("ppt/" + tgt)
        elif tgt.startswith("notesMasters/") or tgt.startswith("handoutMasters/"):
            referenced.add("ppt/" + tgt)
        elif tgt.startswith("media/"):
            referenced.add("ppt/" + tgt)
        else:
            referenced.add("ppt/" + tgt)
referenced.update({"ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"})

# 只有明确的孤儿才删：ppt/tags/ 下未被引用的
drop = [n for n in names if n.startswith("ppt/tags/") and n not in referenced]
# 确保 entry 本身（ppt/tags）不误删
drop = [n for n in drop if not n.endswith("/")]
print("删除孤儿 tag parts:", drop)

with zipfile.ZipFile(TMP, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in sorted(data.keys()):
        if n in drop:
            continue
        zout.writestr(n, data[n])

os.replace(TMP, SRC)
print("\n重建完成:", SRC)
