#!/usr/bin/env python3
"""
修改 PMCF Plan - No comparator section
文字被<w:lastRenderedPageBreak/>分成了两个<w:t>元素，需要分别处理
"""

xml_path = "assets/pmcf_unpacked/word/document.xml"

with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# 原来的第一部分
old_part1 = """<w:t xml:space="preserve">The sample size and endpoints of this survey are defined based on state-of-the-art information, results from the Clinical Evaluation Report, and the device risk management process. Considering the clinical application of the Non-invasive Cerebral Oximetry System, including its tissue oximetry sensor, the survey design, timescale, and target population are appropriate to capture representative real-world feedback. No comparator is required, as the </w:t>"""

# 新的第一部分 - 结束于 "as the"
new_part1 = """<w:t xml:space="preserve">The sample size and endpoints of this survey are defined based on state-of-the-art information, results from the Clinical Evaluation Report, and the device risk management process. Considering the clinical application of the Non-invasive Cerebral Oximetry System, including its tissue oximetry sensor, the survey design, timescale, and target population are appropriate to capture representative real-world feedback. No comparator is required, as </w:t>"""

# 原来的第二部分
old_part2 = """<w:lastRenderedPageBreak/><w:t>objective is to confirm safety, usability, and performance in daily clinical practice. Adequate control measures and statistical methods will ensure data reliability and minimize bias; therefore, this PMCF activity is scientifically justified and without significant limitations.</w:t>"""

# 新的第二部分 - 改为HCP主观确认路径
new_part2 = """<w:t>prospective controlled comparison against a reference standard (e.g., blood gas analyzer) is not feasible or ethically justified in the post-market setting—patients cannot be subjected to additional testing solely for PMCF purposes. Measurement accuracy is verified through HCP subjective confirmation during routine clinical use, which is an accepted PMCF method under MDCG 2020-7. The primary endpoint threshold (p0 = 70%) is set conservatively to account for the absence of a controlled comparison, ensuring that the target is achievable through HCP confirmation alone. This PMCF activity is scientifically justified and without significant limitations.</w:t>"""

if old_part1 in content:
    content = content.replace(old_part1, new_part1)
    changes.append("✓ 修改2a: No comparator section 第一部分 - 已更新")
else:
    changes.append("✗ 修改2a: 未找到第一部分原文")

if old_part2 in content:
    content = content.replace(old_part2, new_part2)
    changes.append("✓ 修改2b: No comparator section 第二部分 - 已改为HCP主观确认路径，删除回顾性分析")
else:
    changes.append("✗ 修改2b: 未找到第二部分原文")

# 输出结果
print("=" * 60)
print("PMCF Plan 修改报告 - Part 2")
print("=" * 60)
for c in changes:
    print(c)
print("=" * 60)

# 保存
with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n文件已保存: {xml_path}")
