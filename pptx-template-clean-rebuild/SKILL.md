---
name: pptx-template-clean-rebuild
description: python-pptx 以「含 slide 的模板」为源、清空后重排新页时，产出的 .pptx 在 PowerPoint/预览引擎中空白。本技能修复该问题：去重 zip 重名 slide part + 重写 presentation.xml.rels 剔除孤儿 slide 引用。触发词：PPT 空白、模板生成 pptx 打不开、python-pptx 清除模板 slide、presentation.xml.rels 重复 slide、rId 泄漏。
---

# pptx-template-clean-rebuild

## 问题
用 `python-pptx` 打开一个**自带 slide 的模板**（如 PPT template.pptx），然后清空 `sldIdLst` 再 `add_slide` 新增 N 页，保存后会出现两种被严格解析器（PowerPoint / 腾讯文档预览）判为损坏的现象：

1. **整份空白**：zip 内 `ppt/slides/slide1.xml` 出现两个同名条目（模板孤儿 part + 新页 part 重名）。
2. **2-29 页空白，仅封面正常**：`ppt/_rels/presentation.xml.rels` 里两条 slide 关系同时指向 `slides/slide1.xml`（`rId3` 孤儿引用残留 + `rId11` 新引用）。

这两种都让 PowerPoint 拒绝渲染。而 **LibreOffice 往往能渲染出内容**——所以只要「LibreOffice 正常但 PowerPoint/预览空白」，几乎可断定是包结构问题，不是数据丢失。

## 根因
`prs.slides._sldIdLst.remove(slide)` 只删了 sldIdLst 里的条目，**不删除 slide 的 part 与 rels**。于是：
- 孤儿 `ppt/slides/slide1.xml` 仍在 zip，与新页重名；
- 孤儿关系 `rId3 → slides/slide1.xml` 残留于 presentation.xml.rels。

## 修复流程（两步，缺一不可）

### 步骤 1：去重 zip 重名条目（保留最后一次写入）
```python
import zipfile
path = "out.pptx"; tmp = "out_tmp.pptx"
with zipfile.ZipFile(path, "r") as zin:
    infolist = zin.infolist()
    last_idx = {}
    for i, info in enumerate(infolist):
        last_idx[info.filename] = i
    keep = [i for i in range(len(infolist)) if i in set(last_idx.values())]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in keep:
            info = infolist[i]
            zi = zipfile.ZipInfo(info.filename, info.date_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zout.writestr(zi, zin.read(info.filename))
os.replace(tmp, path)
```

### 步骤 2：重写 presentation.xml.rels + presententation.xml
读取 `ppt/_rels/presentation.xml.rels` 与 `ppt/presentation.xml`：
- 解析全部 `<Relationship>`，区分类型为 `/slide` 与非 slide；
- 非 slide 关系原样保留；
- 按 `sldIdLst` 中 `<p:sldId r:id="...">` 的顺序，给 slide 重新分配**连续且唯一**的 rId，只保留这 N 条 slide 关系（**剔除孤儿**如 rId3）；
- **关键：slide 的新 rId 绝不能与非 slide 关系撞号。** 非 slide 关系（`notesMaster`/`handoutMaster`/`presProps`/`viewProps`/`tableStyles`/`commentAuthors`/`tags`）常占用 `rId32..rId38` 这类高位 Id——若把 slide 硬编号为 `rId11..rId39`，会从第 22 页起与非 slide 关系 rId 冲突，导致**第 22-28 页黑屏/空白、其余页正常**（LibreOffice 与 PowerPoint 一致）。正确做法：slide 新 Id 从 `max(非slide关系数字Id) + 1` 开始，或对全部关系统一连续重编号并同步更新 presentation.xml 里的 `sldMasterId`/`notesMasterId` 等引用。
- 重建 `sldIdLst`（id 从 256 递增）引用新 rId。

完整可运行脚本见同目录 `rebuild_clean.py`（已含步骤 1+2，`os.replace` 原子覆盖）。

## 固化
把这两步封装进生成脚本的保存后处理函数（如 `_finalize_package(path)`），在 `prs.save()` 之后调用。此后一条命令即产干净成品，不再需要手动去重/清理。

## 验证
- `slide1.xml` 在 zip 中条目数 == 1
- presentation.xml.rels 的 slide 引用去重后数量 == 页数
- sldIdLst 页数 == 页数
- LibreOffice `--convert-to pdf` + `pdftoppm` 渲染全部页，覆盖率 > 5%（无空白）

## 教训
凡「模板本身含 slide」再清空重排的 python-pptx 生成，**必须**做 rels 清理，否则 PowerPoint 严格校验必挂。判断症状：LibreOffice 渲染正常 + PowerPoint/预览空白 → 查 rels 重复 slide 引用。
