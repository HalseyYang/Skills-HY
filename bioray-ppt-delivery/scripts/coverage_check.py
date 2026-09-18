#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PPT 覆盖率自检 —— LibreOffice → PDF → PNG → 量化非白像素占比

用法:
    python coverage_check.py <file.pptx> [--threshold 0.40] [--summary-threshold 0.20]
    python coverage_check.py <file.pptx> --pages 1,12,20        # 只查指定页

输出:
    每页非白像素占比 + 是否达标判定；退出码 1 表示有页不达标。

依赖:
    - LibreOffice (soffice) 在 PATH 或常见安装路径
    - PyMuPDF (pip install pymupdf)  或 pdf2image + poppler
    - Pillow
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')

SOFFICE_CANDIDATES = [
    'soffice',
    'libreoffice',
    r'C:\Program Files\LibreOffice\program\soffice.exe',
    r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
]

# 接近白的判定：三通道均 >= 245
WHITE_CUTOFF = 245


def find_soffice():
    for c in SOFFICE_CANDIDATES:
        if os.path.isabs(c):
            if os.path.isfile(c):
                return c
        else:
            p = shutil.which(c)
            if p:
                return p
    return None


def pptx_to_pdf(soffice, pptx, outdir):
    cmd = [soffice, '--headless', '--convert-to', 'pdf', '--outdir', outdir, pptx]
    subprocess.run(cmd, check=True, capture_output=True, timeout=600)
    base = os.path.splitext(os.path.basename(pptx))[0] + '.pdf'
    out = os.path.join(outdir, base)
    if not os.path.isfile(out):
        raise RuntimeError('PDF 未生成: ' + out)
    return out


def pdf_to_images(pdf, outdir, dpi=100):
    """优先 PyMuPDF，回退 pdf2image。"""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf)
        paths = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            p = os.path.join(outdir, 'page_%03d.png' % (i + 1))
            pix.save(p)
            paths.append(p)
        doc.close()
        return paths
    except ImportError:
        pass

    try:
        from pdf2image import convert_from_path
    except ImportError:
        raise RuntimeError('需要 PyMuPDF 或 pdf2image，请安装: pip install pymupdf')

    imgs = convert_from_path(pdf, dpi=dpi)
    paths = []
    for i, im in enumerate(imgs):
        p = os.path.join(outdir, 'page_%03d.png' % (i + 1))
        im.save(p)
        paths.append(p)
    return paths


def nonwhite_ratio(png):
    from PIL import Image
    im = Image.open(png).convert('RGB')
    w, h = im.size
    px = im.load()
    nonwhite = 0
    total = w * h
    # 抽样加速：步长为 2 时约 1/4 像素
    step = 2 if total > 2_000_000 else 1
    sampled = 0
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            sampled += 1
            if not (r >= WHITE_CUTOFF and g >= WHITE_CUTOFF and b >= WHITE_CUTOFF):
                nonwhite += 1
    return nonwhite / sampled if sampled else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx')
    ap.add_argument('--threshold', type=float, default=0.40, help='内容页下限，默认 0.40')
    ap.add_argument('--summary-threshold', type=float, default=0.20, help='总结/时间轴页下限，默认 0.20')
    ap.add_argument('--pages', default='', help='只查指定页，如 1,12,20')
    ap.add_argument('--summary-pages', default='', help='指定哪些页按总结阈值判定，如 11,20')
    ap.add_argument('--dpi', type=int, default=100)
    args = ap.parse_args()

    if not os.path.isfile(args.pptx):
        print('文件不存在:', args.pptx)
        return 2

    soffice = find_soffice()
    if not soffice:
        print('未找到 LibreOffice (soffice)，请安装或加入 PATH')
        return 2

    only = set(int(x) for x in args.pages.split(',') if x.strip()) if args.pages else None
    summary = set(int(x) for x in args.summary_pages.split(',') if x.strip())

    tmp = tempfile.mkdtemp(prefix='ppt_coverage_')
    try:
        print('[1/3] PPTX → PDF ...')
        pdf = pptx_to_pdf(soffice, args.pptx, tmp)

        print('[2/3] PDF → PNG ...')
        imgs = pdf_to_images(pdf, tmp, dpi=args.dpi)

        print('[3/3] 量化非白像素占比 ...')
        print()
        print('%-8s %-12s %-10s %s' % ('页码', '非白占比', '阈值', '判定'))
        print('-' * 46)

        failed = []
        for i, png in enumerate(imgs, start=1):
            if only is not None and i not in only:
                continue
            ratio = nonwhite_ratio(png)
            thr = args.summary_threshold if i in summary else args.threshold
            ok = ratio >= thr
            if not ok:
                failed.append(i)
            print('%-8d %-12s %-10s %s' % (
                i, '%.1f%%' % (ratio * 100), '%.0f%%' % (thr * 100),
                'OK' if ok else '✗ 偏低'))

        print()
        if failed:
            print('不达标页:', ', '.join(str(x) for x in failed))
            print('→ 先修这些页再交付')
            return 1
        print('全部达标 ✓')
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
