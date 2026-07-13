with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# Update revision history: Add A/2 entry
# Find the A/1 row in the revision table
OLD_REV_A1 = '''<w:t>A/1</w:t>
      </w:r>
    </w:p>
          </w:tc>
          <w:tc>
            <w:tcPr>
              <w:tcW w:w="0" w:type="auto"/>
              <w:tcBorders>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
              </w:tcBorders>
              <w:tcMar>
                <w:top w:w="0" w:type="dxa"/>
                <w:left w:w="113" w:type="dxa"/>
                <w:bottom w:w="0" w:type="dxa"/>
                <w:right w:w="113" w:type="dxa"/>
              </w:tcMar>
            </w:tcPr>
            <w:p w14:paraId="6B48A197" w14:textId="2E013848" w:rsidR="00A35FDA" w:rsidRDefault="00000000" w:rsidP="00343219">'''

# Check if it's there
if OLD_REV_A1 in content:
    print("Revision A/1 row found, updating...")
else:
    print("Revision row not found with exact match, looking for simpler anchor...")
    idx = content.find('2025.08.29')
    print(f"2025.08.29 at idx: {idx}")
    if idx >= 0:
        print(repr(content[idx-100:idx+200]))
