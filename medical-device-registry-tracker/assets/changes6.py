with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ============================================================
# CHANGE 6a: Fix rSO2 cerebral measurement range
# OLD: "Cerebral blood oxygen saturation measurement range: 50% to 100%."
# NEW: "Cerebral blood oxygen saturation (rSO2) measurement range: 70% to 100%. Accuracy: ±2%."
# ============================================================
OLD_RSO2 = ' Cerebral blood oxygen saturation measurement range: 50% to 100%. '
NEW_RSO2 = ' Cerebral blood oxygen saturation (rSO\u2082) measurement range: 70% to 100%. Accuracy: \u00b12%.'

if OLD_RSO2 in content:
    content = content.replace(OLD_RSO2, NEW_RSO2)
    changes += 1
    print("CHANGE 6a (rSO2 range) applied")
else:
    print("CHANGE 6a: rSO2 text not found")
    idx = content.find('Cerebral blood oxygen saturation measurement range')
    if idx >= 0:
        print(f"  Found partial at {idx}: {repr(content[idx:idx+100])}")

# ============================================================
# CHANGE 6b: Fix StO2 tissue measurement range  
# OLD: "Tissue oxygen saturation measurement range: 50% to 100%."
# NEW: "Tissue blood oxygen saturation (StO2) measurement range: 70% to 100%. Accuracy: ±2%."
# ============================================================
OLD_STO2 = 'Tissue oxygen saturation measurement range: 50% to 100%.'
NEW_STO2 = 'Tissue blood oxygen saturation (StO\u2082) measurement range: 70% to 100%. Accuracy: \u00b12%.'

if OLD_STO2 in content:
    content = content.replace(OLD_STO2, NEW_STO2)
    changes += 1
    print("CHANGE 6b (StO2 range) applied")
else:
    print("CHANGE 6b: StO2 text not found")
    idx = content.find('Tissue oxygen saturation measurement range')
    if idx >= 0:
        print(f"  Found partial at {idx}: {repr(content[idx:idx+100])}")

# ============================================================
# CHANGE 6c: Fix SpO2 pulse oximetry range
# OLD: "Range of oxygen saturation measurement of finger pulse: 70% to 100%. The tolerance is ± 1%."
# NEW: "Pulse oxygen saturation (SpO2) measurement range: 50% to 90%. Accuracy: ±2%."
# ============================================================
OLD_SPO2_VARIANTS = [
    'Range of oxygen saturation measurement of finger pulse: 70% to 100%. The tolerance is \u00b1 1%.',
    'Range of oxygen saturation measurement of finger pulse: 70% to 100%. The tolerance is \u00b11%.',
]
NEW_SPO2 = 'Pulse oxygen saturation (SpO\u2082) measurement range: 50% to 90%. Accuracy: \u00b12%.'

found_spo2 = False
for OLD_SPO2 in OLD_SPO2_VARIANTS:
    if OLD_SPO2 in content:
        content = content.replace(OLD_SPO2, NEW_SPO2)
        changes += 1
        print(f"CHANGE 6c (SpO2 range) applied")
        found_spo2 = True
        break

if not found_spo2:
    idx = content.find('Range of oxygen saturation measurement of finger pulse')
    if idx >= 0:
        print(f"CHANGE 6c: Found at {idx}: {repr(content[idx:idx+150])}")
        # Do a simpler replacement
        old_frag = content[idx:idx+150]
        print(f"Exact text: {repr(old_frag)}")
    else:
        print("CHANGE 6c: SpO2 text not found at all")
        # Search for tolerance text
        idx2 = content.find('tolerance is')
        if idx2 >= 0:
            print(f"  Found 'tolerance is' at {idx2}: {repr(content[idx2-50:idx2+100])}")

# ============================================================
# CHANGE 6d: Fix alarm tolerance reference in questionnaire
# OLD: "alarm error: Tolerance: ± 1%, effectiveness"
# Keep this unchanged as it's about alarm tolerance not measurement range
# ============================================================

with open('c:/Users/ThinkBook/.workbuddy/skills/medical-device-registry-tracker/assets/pmcf_unpacked/word/document.xml', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Total changes: {changes}")
