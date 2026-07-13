with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ========== CHANGE 4: 在 "Objective" 段落后面增加 Endpoints 段落 ==========
# 找到 "Objective" heading 紧接的那个包含objective文本的段落，在其后插入 Endpoints 段落

ENDPOINT_PARA_RUN = '''<w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:eastAsiaTheme="minorEastAsia" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>'''

RUN_TEMPLATE = f'''    <w:p w14:paraId="6854AB01" w14:textId="AAAAAAAA" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t>PMCF Survey Endpoints</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB02" w14:textId="AAAAAAAB" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t xml:space="preserve">Primary Endpoints</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB03" w14:textId="AAAAAAAC" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
        <w:t xml:space="preserve">(1) Measurement Accuracy (Clinical Performance). HCPs are asked to evaluate whether the device measurements fall within the specified accuracy tolerances during routine clinical use, corresponding to the following GSPR-linked performance parameters: SpO2 accuracy: \u00b12% (measurement range 50\u201390%); StO2 (tissue blood oxygen saturation) accuracy: \u00b12% (measurement range 70\u2013100%); rSO2 (cerebral blood oxygen saturation) accuracy: \u00b12% (measurement range 70\u2013100%). The proportion of respondents confirming that measurements are within the specified accuracy tolerances must meet or exceed the pre-defined target value (p0 = 70%). This endpoint directly supports the safety and performance conclusions of the CER (ZKBK-TR-NC-028 V A/1) regarding GSPR 14 (measurement accuracy and precision). (2) Clinical Performance in Intended Use. HCPs are asked to assess whether the device provides clinically reliable, continuous, and real-time haemodynamic monitoring in the intended clinical settings (operating room, ICU, neurosurgery, cardiac surgery). The proportion of respondents confirming satisfactory clinical performance must meet or exceed p0 = 70%.</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB04" w14:textId="AAAAAAAD" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t xml:space="preserve">Secondary Endpoint</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB05" w14:textId="AAAAAAAE" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
        <w:t xml:space="preserve">Adverse Event Incidence Rate. HCPs are requested to report any device-related adverse events (including intraoperative, immediate postoperative, and rare/delayed adverse events) observed during clinical use. The adverse event incidence rate will be calculated as: (number of respondents reporting at least one adverse event / total number of evaluable responses) x 100%. A rate below the pre-specified safety threshold (consistent with the acceptable risk level established in the risk management file ZKBK-TR-NC-030) is required to confirm continued benefit-risk acceptability.</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB06" w14:textId="AAAAAAAF" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
          <w:b/>
          <w:bCs/>
          <w:color w:val="auto"/>
          <w:kern w:val="2"/>
          <w:sz w:val="21"/>
          <w:szCs w:val="22"/>
        </w:rPr>
        <w:t xml:space="preserve">Relationship between PMCF Survey Results and CER Endpoints throughout the Device Lifetime</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AB07" w14:textId="AAAAAAAG" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
        <w:t xml:space="preserve">The device has an expected service lifetime of 5 years. The PMCF survey is designed to continuously verify safety and performance throughout this period as follows. Annual data collection: survey data will be collected and analysed annually throughout the 5-year PMCF period. Each annual cohort (n = 64) provides an independent assessment of real-world performance and safety. Endpoint linkage to CER: the primary endpoint (measurement accuracy of SpO2, StO2, and rSO2) directly corresponds to the performance endpoints confirmed in the CER and the GSPR 14 measurement accuracy requirements; the secondary endpoint (adverse event incidence) supports the safety conclusion of the CER and the residual risk acceptability established in the risk management file. Annual PMCF evaluation reports will document whether the pre-specified endpoints are met, and will be reflected in the annual PSUR. Any clinically significant trend (e.g., declining accuracy confirmation rate or increase in reported adverse events) will trigger a CER update and, if necessary, corrective actions per the risk management procedure (ZKBK-TR-NC-030). Monitoring over expected lifetime: because the PMCF period spans the full 5-year device lifetime, data collected in Years 1\u20135 collectively verify that device safety and performance remain acceptable throughout the expected service life. Cumulative analysis of all annual cohorts (\u2248320 responses) will be performed in the final PMCF Evaluation Report to confirm that performance and safety endpoints defined in the CER are continuously satisfied from market launch through end of expected lifetime.</w:t>
      </w:r>
    </w:p>
'''

# Insert the endpoint paragraphs AFTER the "Objective" paragraph
# The Objective paragraph ends just before "Target Participants"
TARGET_PARA_ANCHOR = '<w:t>Target Participants</w:t>'
idx_target = content.find(TARGET_PARA_ANCHOR)
if idx_target >= 0:
    # Find start of Target Participants paragraph
    p_target_start = content.rfind('<w:p ', 0, idx_target)
    # Insert endpoint paragraphs before Target Participants
    content = content[:p_target_start] + RUN_TEMPLATE + content[p_target_start:]
    changes += 1
    print("CHANGE 4 (PMCF endpoints) applied")
else:
    print(f"CHANGE 4: Target Participants anchor not found")

with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Total changes: {changes}")
