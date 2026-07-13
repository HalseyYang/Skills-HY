with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# CHANGE 6: 修正调查问卷中的测量范围
# 原文: "Cerebral blood oxygen saturation measurement range: 50% to 100%."
#       "Tissue oxygen saturation measurement range: 50% to 100%."
#       "Range of oxygen saturation measurement of finger pulse: 70% to 100%. The tolerance is ±1%."
# 正确规格:
#   rSO2 (cerebral): 70-100%, accuracy ±2%
#   StO2 (tissue): 70-100%, accuracy ±2%
#   SpO2 (finger/pulse): 50-90%, accuracy ±2%
# ============================================================

OLD_ACCURACY_LINE = '<w:t xml:space="preserve">&#x2610;  Cerebral blood oxygen saturation measurement range: 50% to 100%. </w:t>\n      </w:r>\n      <w:r>\n        <w:rPr>\n          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:hint="eastAsia"/>\n          <w:color w:val="auto"/>\n          <w:kern w:val="2"/>\n          <w:sz w:val="21"/>\n          <w:szCs w:val="22"/>\n        </w:rPr>\n        <w:t xml:space="preserve">&#x2610;  Tissue oxygen saturation measurement range: 50% to 100%.  &#x2610;  Range of oxygen saturation measurement of finger pulse: 70% to 100%. The tolerance is \u00b1 1%.</w:t>'

idx_accuracy = content.find('Cerebral blood oxygen saturation measurement range: 50% to 100%')
if idx_accuracy >= 0:
    p_start = content.rfind('<w:p ', 0, idx_accuracy)
    p_end = content.find('</w:p>', idx_accuracy) + len('</w:p>')
    print(f"Accuracy para found at {p_start}-{p_end}")
    print("OLD PARA:")
    print(repr(content[p_start:p_end]))
else:
    print("Accuracy line NOT found")

with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Done")
