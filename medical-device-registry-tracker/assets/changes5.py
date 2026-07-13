with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# CHANGE 5a: 删除问卷中的 "Neonatal department" 选项
# ============================================================
# 原文: checkboxes in questionnaire include neonatal department
OLD_NEONATAL_PARA = '''    <w:p w14:paraId="70F28AD4" w14:textId="77777777" w:rsidR="006141F6" w:rsidRDefault="006141F6" w:rsidP="00343219">
      <w:pPr>
        <w:pStyle w:val="Default"/>
        <w:spacing w:beforeLines="50" w:before="156" w:afterLines="50" w:after="156" w:line="276" w:lineRule="auto"/>
        <w:jc w:val="both"/>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t xml:space="preserve">&#x2610;  Neonatal department </w:t>
      </w:r>
    </w:p>'''

# Search for neonatal department text in the questionnaire
idx_neonatal = content.find('Neonatal department')
if idx_neonatal >= 0:
    p_start = content.rfind('<w:p ', 0, idx_neonatal)
    p_end = content.find('</w:p>', idx_neonatal) + len('</w:p>')
    actual_para = content[p_start:p_end]
    content = content[:p_start] + content[p_end:]
    changes += 1
    print(f"CHANGE 5a (delete Neonatal department) applied, removed para at {p_start}-{p_end}")
else:
    print("CHANGE 5a: Neonatal department NOT found")

# ============================================================
# CHANGE 5b: 修改 C.2.2 Aim 部分 - 增加对 off-label use 防范措施描述
# 在 Section C.2.3 Rationale 段落后添加 off-label use 防范段落
# ============================================================
# Find C.2.3 Rationale paragraph
OLD_RATIONALE = 'The sample size and endpoints of this survey are defined based on state-of-the-art information'
idx_rationale = content.find(OLD_RATIONALE)
if idx_rationale >= 0:
    p_start = content.rfind('<w:p ', 0, idx_rationale)
    p_end = content.find('</w:p>', idx_rationale) + len('</w:p>')
    
    OFFLABEL_PARAS = '''
    <w:p w14:paraId="6854AC01" w14:textId="BBBBBBBB" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
      <w:pPr>
        <w:pStyle w:val="Default"/>
        <w:spacing w:beforeLines="50" w:before="156" w:afterLines="50" w:after="156" w:line="276" w:lineRule="auto"/>
        <w:jc w:val="both"/>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t>Measures to Prevent Off-label Use</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AC02" w14:textId="BBBBBBBC" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
      <w:pPr>
        <w:pStyle w:val="Default"/>
        <w:spacing w:beforeLines="50" w:before="156" w:afterLines="50" w:after="156" w:line="276" w:lineRule="auto"/>
        <w:jc w:val="both"/>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t xml:space="preserve">The Non-invasive Cerebral Oximetry System is intended exclusively for use in adult patients. The following measures are implemented to prevent off-label use, in particular use in paediatric or neonatal patients: (1) Exclusion criteria in PMCF survey: the PMCF survey questionnaire explicitly restricts participation to HCPs who use the device within its CE-marked intended purpose (adult patients). The survey instructions clearly state that the device is not indicated for use in neonatal or paediatric populations, and respondents from neonatal departments are excluded from the survey. (2) Labelling and Instructions for Use (IFU): the IFU and device labelling clearly specify that the device is intended only for adult patients, and include explicit contraindications against use in paediatric or neonatal patients. These restrictions are reviewed as part of the annual PMCF evaluation cycle. (3) User training records: the manufacturer requires that authorised distributors provide device-specific training to clinical users prior to first use. Training materials include clear communication of the approved intended purpose and patient population. Training completion records are maintained by the manufacturer and reviewed annually. (4) Monitoring through PMCF survey and reactive PMS: the PMCF survey includes a specific question to identify whether any off-label use has been observed or reported (Section C.2.2, Aim: &#x201C;identifying possible systematic misuse or off-label use of the device&#x201D;). Any report of off-label use will be escalated for immediate evaluation through the CAPA process and reflected in the PSUR update.</w:t>
      </w:r>
    </w:p>
'''
    # Insert after C.2.3 rationale paragraph
    content = content[:p_end] + OFFLABEL_PARAS + content[p_end:]
    changes += 1
    print(f"CHANGE 5b (off-label prevention measures) applied")
else:
    print("CHANGE 5b: rationale anchor not found")

with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Changes applied: {changes}")
