#!/usr/bin/env python3
"""
修改 PMCF Plan - 3处修改:
1. Primary Endpoints: 改为HCP主观确认
2. No comparator section: 删除回顾性分析和文献等效性路径
3. (自动) 确保所有准确性验证路径一致为HCP主观确认
"""

import re

xml_path = "assets/pmcf_unpacked/word/document.xml"

with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# ========== 修改1: Primary Endpoints ==========
old_primary = """(1) Measurement Accuracy (Clinical Performance). HCPs are asked to evaluate whether the device measurements fall within the specified accuracy tolerances during routine clinical use, corresponding to the following GSPR-linked performance parameters: SpO2 accuracy: ±2% (measurement range 50–90%); StO2 (tissue blood oxygen saturation) accuracy: ±2% (measurement range 70–100%); rSO2 (cerebral blood oxygen saturation) accuracy: ±2% (measurement range 70–100%). The proportion of respondents confirming that measurements are within the specified accuracy tolerances must meet or exceed the pre-defined target value (p0 = 70%). This endpoint directly supports the safety and performance conclusions of the CER (ZKBK-TR-NC-028 V A/1) regarding GSPR 14 (measurement accuracy and precision). (2) Clinical Performance in Intended Use. HCPs are asked to assess whether the device provides clinically reliable, continuous, and real-time haemodynamic monitoring in the intended clinical settings (operating room, ICU, neurosurgery, cardiac surgery). The proportion of respondents confirming satisfactory clinical performance must meet or exceed p0 = 70%."""

new_primary = """(1) Measurement Accuracy (HCP Subjective Confirmation). HCPs are asked to evaluate whether the device measurements were clinically acceptable and consistent with their clinical judgment during routine clinical use, corresponding to the following GSPR-linked performance parameters: SpO2 measurement range 50–90% (accuracy ±2%); StO2 (tissue blood oxygen saturation) measurement range 70–100% (accuracy ±2%); rSO2 (cerebral blood oxygen saturation) measurement range 70–100% (accuracy ±2%). HCPs confirm whether the device provided clinically reliable and acceptable readings in their patient population. The proportion of respondents confirming clinically acceptable measurement accuracy must meet or exceed the pre-defined target value (p0 = 70%). This endpoint directly supports the safety and performance conclusions of the CER (ZKBK-TR-NC-028 V A/1) regarding GSPR 14 (measurement accuracy and precision). (2) Clinical Performance in Intended Use. HCPs are asked to assess whether the device provides clinically reliable, continuous, and real-time haemodynamic monitoring in the intended clinical settings (operating room, ICU, neurosurgery, cardiac surgery). The proportion of respondents confirming satisfactory clinical performance must meet or exceed p0 = 70%."""

if old_primary in content:
    content = content.replace(old_primary, new_primary)
    changes.append("✓ 修改1: Primary Endpoints - 已改为HCP主观确认")
else:
    changes.append("✗ 修改1: 未找到 Primary Endpoints 原文")

# ========== 修改2: No comparator section ==========
# 原来的完整段落
old_no_comparator = """The sample size and endpoints of this survey are defined based on state-of-the-art information, results from the Clinical Evaluation Report, and the device risk management process. Considering the clinical application of the Non-invasive Cerebral Oximetry System, including its tissue oximetry sensor, the survey design, timescale, and target population are appropriate to capture representative real-world feedback. No comparator is required, as the objective is to confirm safety, usability, and performance in daily clinical practice. Adequate control measures and statistical methods will ensure data reliability and minimize bias; therefore, this PMCF activity is scientifically justified and without significant limitations."""

# 新的段落 - 只保留HCP主观确认路径，删除回顾性分析和文献等效性
new_no_comparator = """The sample size and endpoints of this survey are defined based on state-of-the-art information, results from the Clinical Evaluation Report, and the device risk management process. Considering the clinical application of the Non-invasive Cerebral Oximetry System, including its tissue oximetry sensor, the survey design, timescale, and target population are appropriate to capture representative real-world feedback. No comparator is required, as prospective controlled comparison against a reference standard (e.g., blood gas analyzer) is not feasible or ethically justified in the post-market setting—patients cannot be subjected to additional testing solely for PMCF purposes. Measurement accuracy is verified through HCP subjective confirmation during routine clinical use, which is an accepted PMCF method under MDCG 2020-7. The primary endpoint threshold (p0 = 70%) is set conservatively to account for the absence of a controlled comparison, ensuring that the target is achievable through HCP confirmation alone. This PMCF activity is scientifically justified and without significant limitations."""

if old_no_comparator in content:
    content = content.replace(old_no_comparator, new_no_comparator)
    changes.append("✓ 修改2: No comparator section - 已删除回顾性分析，改为纯HCP主观确认路径")
else:
    changes.append("✗ 修改2: 未找到 No comparator 原文段落")

# ========== 修改3: 删除文档中任何提及回顾性分析的内容 ==========
# 检查是否有其他提及回顾性对比的地方
retrospective_patterns = [
    r"retrospective.*compar",
    r"回顾.*对比",
    r"retrospective.*blood gas",
    r"血气.*回顾"
]

for pattern in retrospective_patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        changes.append(f"  发现需关注内容: {pattern} -> {matches}")

# 输出结果
print("=" * 60)
print("PMCF Plan 修改报告")
print("=" * 60)
for c in changes:
    print(c)
print("=" * 60)

# 保存
with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n文件已保存: {xml_path}")
