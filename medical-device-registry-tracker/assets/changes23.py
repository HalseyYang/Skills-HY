with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ========== CHANGE 2: EU patient population ==========
OLD_TARGET = '<w:t>Licensed health care professionals with direct experience in using the subject device in clinical settings (e.g., anesthesiologists, intensivists, neurosurgeons, critical care nurses).</w:t>'
NEW_TARGET = '<w:t xml:space="preserve">Licensed health care professionals with direct experience in using the subject device in clinical settings (e.g., anesthesiologists, intensivists, neurosurgeons, critical care nurses). To ensure representative coverage of the EU-intended patient population, at least 30% of survey respondents (i.e., a minimum of 20 respondents per annual collection cycle) shall be recruited from healthcare institutions located within the European Union (EU). This quota is based on the proportion of EU sales relative to total global sales (EU: 3,327 units / Total: 10,159 units, representing approximately 32.75% of global distribution). EU respondent data will be analysed separately to confirm device performance and safety in the EU intended use environment.</w:t>'

if OLD_TARGET in content:
    content = content.replace(OLD_TARGET, NEW_TARGET)
    changes += 1
    print("CHANGE 2 (EU population) applied")
else:
    idx = content.find('Licensed health care professionals with direct experience')
    print(f"CHANGE 2 NOT FOUND. idx={idx}")

# ========== CHANGE 3: sample size replacement ==========
idx_heading = content.find('The Sample size is calculated as follow:')
idx_result = content.find('After calculation, the sample size should be ')
idx_result_end = content.find('</w:p>', idx_result) + len('</w:p>')
p_heading_start = content.rfind('<w:p ', 0, idx_heading)

print(f"Sample block: {p_heading_start} to {idx_result_end}")

OLD_SAMPLE_BLOCK = content[p_heading_start:idx_result_end]

NEW_SAMPLE_BLOCK = '''<w:p w14:paraId="6854AAAC" w14:textId="11111111" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
        <w:t xml:space="preserve">The sample size is calculated using the one-sample proportion test (single-group target value method), which is appropriate for PMCF surveys where a minimum acceptable performance threshold (target value) is pre-specified. The sample size formula is: n = (Z\u03b1 \u221a[p\u2080(1\u2212p\u2080)] + Z\u03b2 \u221a[p\u2081(1\u2212p\u2081)])\u00b2 / (p\u2081 \u2212 p\u2080)\u00b2</w:t>
      </w:r>
    </w:p>
    <w:p w14:paraId="6854AAAE" w14:textId="11111113" w:rsidR="00BB5BDB" w:rsidRDefault="00BB5BDB" w:rsidP="00BB5BDB">
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
        <w:t xml:space="preserve">Note: n = required sample size per annual collection cycle; p\u2080 = target value (minimum acceptable rate of satisfactory clinical performance) = 0.70 (70%); p\u2081 = expected actual performance rate = 0.85 (85%), based on existing clinical investigation data and PMS records; Z\u03b1 = 1.960 (two-sided \u03b1 = 0.05); Z\u03b2 = 0.842 (power = 80%). Calculation: n = (1.960 \u00d7 \u221a[0.70 \u00d7 0.30] + 0.842 \u00d7 \u221a[0.85 \u00d7 0.15])\u00b2 / (0.85 \u2212 0.70)\u00b2 = 63.88, rounded up to n = 64 per annual collection cycle. The required annual sample size is 64 cases (per year); over the 5-year PMCF period, the cumulative total will be approximately 320 responses. Of the 64 annual responses, at least 20 (\u226530%) shall be from EU-based healthcare institutions to ensure the EU patient population is adequately represented.</w:t>
      </w:r>
    </w:p>'''

content = content[:p_heading_start] + NEW_SAMPLE_BLOCK + content[idx_result_end:]
changes += 1
print("CHANGE 3 (sample size) applied")

with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Total changes: {changes}")
