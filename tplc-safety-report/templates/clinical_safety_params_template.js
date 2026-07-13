const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, WidthType, BorderStyle, ShadingType, VerticalAlign } = require('docx');
const fs = require('fs');

// ===== Format constants matching step_06.docx =====
const FONT = "Times New Roman";
const FONT_EA = "SimSun";
const SZ_SECTION = 24;
const SZ_SUB = 22;
const SZ_BODY = 21;
const INDENT_BODY = 400;
const LINE_SPACING = 240;

const border = { style: BorderStyle.SINGLE, size: 4, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
const HDR_FILL = "F0F0F0";

function sectionHeading(text) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, lineRule: "auto", before: 120, after: 120 },
    children: [new TextRun({ text, font: FONT, fonts: { eastAsia: FONT_EA }, bold: true, color: "000000", size: SZ_SECTION })],
  });
}
function subHeading(text) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, lineRule: "auto", before: 120, after: 120 },
    children: [new TextRun({ text, font: FONT, fonts: { eastAsia: FONT_EA }, bold: true, color: "000000", size: SZ_SUB })],
  });
}
function bodyPara(text) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, lineRule: "auto", after: 40 },
    indent: { left: INDENT_BODY },
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, font: FONT, fonts: { eastAsia: FONT_EA }, bold: false, color: "000000", size: SZ_BODY })],
  });
}
function bodyParaRuns(runs) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, lineRule: "auto", after: 40 },
    indent: { left: INDENT_BODY },
    alignment: AlignmentType.JUSTIFIED,
    children: runs.map(r => new TextRun({
      font: FONT, fonts: { eastAsia: FONT_EA }, color: "000000", size: SZ_BODY, bold: r.bold || false, ...r,
    })),
  });
}
function plainPara(text) {
  return new Paragraph({
    spacing: { line: LINE_SPACING, lineRule: "auto", after: 40 },
    children: [new TextRun({ text, font: FONT, fonts: { eastAsia: FONT_EA }, bold: false, color: "000000", size: SZ_BODY })],
  });
}
function hdrCell(text, colSpan) {
  const opts = {
    borders,
    shading: { fill: HDR_FILL, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.TOP,
    children: [new Paragraph({
      spacing: { before: 40, after: 40 },
      children: [new TextRun({ text, font: FONT, fonts: { eastAsia: FONT_EA }, bold: true, color: "000000", size: SZ_BODY })],
    })],
  };
  if (colSpan) opts.columnSpan = colSpan;
  return new TableCell(opts);
}
function dataCell(text, colSpan) {
  const opts = {
    borders,
    verticalAlign: VerticalAlign.TOP,
    children: [new Paragraph({
      spacing: { before: 40, after: 40 },
      children: [new TextRun({ text: String(text), font: FONT, fonts: { eastAsia: FONT_EA }, bold: false, color: "000000", size: SZ_BODY })],
    })],
  };
  if (colSpan) opts.columnSpan = colSpan;
  return new TableCell(opts);
}

// ===== Build document =====
const children = [];

// ---- 5.0 Clinical Safety Parameters ----
children.push(sectionHeading("5.0 Clinical Safety Parameters"));
children.push(bodyPara("This section defines the clinical safety parameters and measurable endpoints for the multi-parameter patient monitoring system, derived exclusively from the post-market safety data analysis presented in Section 6 (Safety Data Report). The safety parameters are structured around the five principal safety signals identified from the FDA TPLC database for product code MHX (2021\u20132026: 14,389 MDR reports, 43 Class II recalls), supplemented by applicable international safety standards. Clinical benefit parameters (e.g., measurement accuracy, diagnostic sensitivity) are addressed separately in Section 4 (Clinical Benefit Assessment) and are not duplicated herein."));

// ---- Table 5-4 Safety Endpoint List ----
children.push(plainPara("Table 5-4 defines the measurable safety endpoints and their acceptance criteria, each traceable to a specific safety signal identified in Section 6 of the Safety Data Report."));

const safetyEndpoints = [
  // Signal 1: Alarm Management (TPLC Section 6.5 + 6.7.1)
  {
    no: "1",
    objective: "Alarm System Reliability \u2014 Audibility and Activation",
    signal: "TPLC Section 6.5: No Audible Alarm (2,393 reports, 17.9%), Defective Alarm (782, 5.8%), Alarm System issues (649, 4.8%), No Audible Prompt (915, 6.8%). Combined: 4,739 alarm-related reports (35.4% of all MDR). Section 6.7.1: Associated with 16 deaths and 187 cardiac arrests.",
    endpoint: "(a) Incidence of alarm non-activation when patient parameter crosses alarm threshold; (b) Incidence of alarm activation without audible output; (c) False alarm rate (alarm triggered without clinical indication); (d) Alarm priority classification accuracy",
    criterion: "(a) Zero incidents of alarm non-activation for high-priority alarms; (b) Alarm non-audibility rate \u2264 0.01% per 1,000 monitoring hours; (c) False alarm rate \u2264 85% of total alarms (industry benchmark per ECRI Institute Top 10 Patient Safety Concerns); (d) Alarm priority correctly assigned for 100% of test scenarios per IEC 60601-1-8:2006+AMD2:2020 Clause 201.6",
    standard: "IEC 60601-1-8:2006+AMD2:2020; ECRI Institute Top 10 Patient Safety Concerns (2014\u20132026); Joint Commission NPSG.06.01.01",
  },
  {
    no: "2",
    objective: "Alarm Fatigue Mitigation",
    signal: "TPLC Section 6.7.1: Alarm-related problems constitute 28.6\u201335.4% of all MDR reports. Section 6.6.1: Fatal and near-fatal events predominantly linked to alarm system failures. Section 6.3: 187 cardiac arrest events and 16 deaths.",
    endpoint: "(a) Non-actionable alarm rate per bed per monitoring shift (8 hours); (b) Clinical staff response time to high-priority alarms; (c) Alarm silence/duration settings compliance with clinical protocol",
    criterion: "(a) Non-actionable alarm rate \u2264 150 per bed per shift (clinical consensus benchmark; Cvach, 2012, PMID: 22839984); (b) Nursing response to high-priority alarms within 60 seconds in \u2265 95% of events; (c) Alarm silence duration \u2264 120 seconds for high-priority alarms per IEC 60601-1-8",
    standard: "IEC 60601-1-8:2006+AMD2:2020; Cvach M. (2012) PMID: 22839984; Sendelbach & Funk (2013) PMID: 24153215; Joint Commission NPSG.06.01.01",
  },
  // Signal 2: Software Stability (TPLC Section 6.5 + 6.7.2)
  {
    no: "3",
    objective: "Software Stability and System Availability",
    signal: "TPLC Section 6.5: Application Program Problem (590 reports, 4.4%), Unexpected Shutdown (405), Program Freeze (388), Unintended Shutdown (416), OS Failures (128), Computer Software Problems (122). Combined: 2,049 software-related reports (15.3%). Section 6.7.2: Software complexity increase with wireless connectivity features.",
    endpoint: "(a) System uptime / availability rate; (b) Unplanned restart frequency per 1,000 monitoring hours; (c) Program freeze/hang events per 1,000 monitoring hours; (d) Software defect rate per software release cycle",
    criterion: "(a) System availability \u2265 99.9% per monitoring period; (b) Unplanned restarts \u2264 0.1 per 1,000 monitoring hours; (c) Program freeze/hang events \u2264 0.05 per 1,000 monitoring hours; (d) No safety-critical software defects (IEC 62304 Class C severity classification) escape to release",
    standard: "IEC 62304:2006+A1:2015 (Class C); IEC 80601-2-49:2018+AMD1:2024",
  },
  {
    no: "4",
    objective: "Display and Visual Feedback Reliability",
    signal: "TPLC Section 6.5: Display or Visual Feedback Problem (670 reports, 5.0%), Output Problem (657 reports, 4.9%). Section 6.6.3: Screen freeze and distorted display may mask critical physiological data.",
    endpoint: "(a) Screen freeze/non-response incidents per 1,000 monitoring hours; (b) Incorrect waveform or trend display events; (c) Visual alarm indicator functionality under ambient lighting conditions",
    criterion: "(a) Screen freeze rate \u2264 0.01 per 1,000 monitoring hours; (b) No incorrect waveform rendering affecting clinical interpretation; (c) Visual alarm indicators functional at \u2265 3 meters in ambient light up to 500 lux per IEC 60601-1-8",
    standard: "IEC 60601-1-8:2006+AMD2:2020; IEC 80601-2-49:2018+AMD1:2024",
  },
  // Signal 3: Communication and Connectivity (TPLC Section 6.5 + 6.7.3)
  {
    no: "5",
    objective: "Communication and Network Data Integrity",
    signal: "TPLC Section 6.5: Communication/Transmission Problem (892 reports, 6.7%), Wireless Communication (318), Intermittent Communication (125). Combined: 1,335 network-related reports (10.0%). Section 6.7.3: Network failures compromise central station monitoring in hospital environments.",
    endpoint: "(a) Data transmission loss rate between bedside monitor and central station; (b) Wireless disconnection frequency per 24-hour monitoring period; (c) Data integrity verification \u2014 no corrupted or missing physiological data packets",
    criterion: "(a) Data loss rate \u2264 0.1% of total data transmissions; (b) Wireless disconnections \u2264 2 per 24-hour period; (c) 100% data packet integrity verification (checksum/CRC); automatic reconnection within 30 seconds",
    standard: "IEC 80601-2-49:2018+AMD1:2024 (Clause 201.12.4.101); IEC 60601-1-6:2010+A2:2020",
  },
  // Signal 4: Skin Integrity (TPLC Section 6.3 + 6.6.2 + 6.7.4)
  {
    no: "6",
    objective: "Skin Integrity and Biocompatibility of Sensors/Electrodes",
    signal: "TPLC Section 6.3: Skin Reactions constitute 1,944 reports (14.5% of patient injuries). Section 6.6.2: Skin inflammation/irritation (1,879), blisters (38), erythema (14), burns (10), skin discoloration (5). Section 6.7.4: Known risk of surface-mounted monitoring sensors.",
    endpoint: "(a) Incidence of Grade \u2265 2 skin injury (erythema, blistering, burn) at electrode/sensor contact sites; (b) Time to onset of skin reaction after sensor application; (c) Thermal injury from temperature sensors",
    criterion: "(a) Grade \u2265 2 skin injury incidence \u2264 0.5% of monitored patients; (b) No Grade \u2265 3 skin injury (blister \u2265 5 mm, full-thickness burn); (c) Zero thermal burns from temperature sensors; biocompatibility compliance per ISO 10993-1:2018 biological evaluation framework",
    standard: "ISO 10993-1:2018; ISO 10993-5:2009 (cytotoxicity); ISO 10993-10:2021 (skin irritation/sensitization)",
  },
  // Signal 5: Power System (TPLC Section 6.5 + 6.7.5)
  {
    no: "7",
    objective: "Power Supply and Battery Backup Reliability",
    signal: "TPLC Section 6.5: Power/Battery/Charging Issues (801 reports, 6.0%). Section 6.6.3: Power problems (285), failure to charge (234), charging problems (167), failure to power up (115), complete power loss (94). Combined: 895 power-related reports (6.7%). Section 6.7.5: Complete monitoring interruption during active monitoring.",
    endpoint: "(a) Battery runtime under full monitoring load (all 8 parameters active); (b) Automatic switchover time from AC to battery; (c) Complete power loss events per 1,000 monitoring hours; (d) Low-battery warning lead time before depletion",
    criterion: "(a) Battery runtime \u2265 30 minutes at full load; (b) Switchover time \u2264 1 second (no monitoring interruption); (c) Complete power loss \u2264 0.05 per 1,000 monitoring hours; (d) Low-battery warning \u2265 5 minutes before full depletion; graceful shutdown with data preservation",
    standard: "IEC 60601-1:2005+AMD2:2020; IEC 80601-2-49:2018+AMD1:2024",
  },
  // Additional: Electrical Safety
  {
    no: "8",
    objective: "Electrical Safety \u2014 Leakage Current and Defibrillation Protection",
    signal: "TPLC Section 6.3: 16 deaths and 187 cardiac arrest events reported. While not all attributable to electrical hazards, the TPLC data underscores the importance of electrical safety for cardiac monitoring equipment applied directly to patients. ECG and IBP sensors constitute applied parts with direct patient contact.",
    endpoint: "(a) Patient leakage current under normal condition (NC) and single fault condition (SFC); (b) Auxiliary leakage current; (c) Defibrillation protection withstand capability; (d) Enclosure leakage current",
    criterion: "(a) Patient leakage current: Type CF \u2264 10 \u00B5A (NC), \u2264 50 \u00B5A (SFC); Type B/BF \u2264 100 \u00B5A (NC), \u2264 500 \u00B5A (SFC) per IEC 60601-1 Table 3; (b) Auxiliary leakage current within Table 4 limits; (c) Defibrillation-proof applied parts withstand per IEC 60601-2-27/IEC 60601-2-49; (d) Enclosure leakage current per Table 2 limits",
    standard: "IEC 60601-1:2005+AMD2:2020 (Tables 2\u20134); IEC 80601-2-49:2018+AMD1:2024",
  },
  // Additional: User Interaction / Use Safety
  {
    no: "9",
    objective: "User Interface Safety and Use Error Prevention",
    signal: "TPLC Section 6.5: Patient Device Interaction Problem (1,648 reports, 12.3%), Incorrect Measurement (338, 2.5%), Unable to Obtain Readings (555, 4.1%). Section 6.6.3: Parameter setting errors, improper device handling, and user interface issues contributing to device malfunction reports.",
    endpoint: "(a) Incidence of user-originated parameter configuration errors; (b) Incidence of sensor connection errors leading to monitoring gaps; (c) Warning/error message clarity assessment \u2014 correct interpretation rate by clinical users",
    criterion: "(a) Parameter configuration error rate \u2264 0.5% of user interactions; (b) Sensor disconnection detection alarm within 10 seconds; (c) Warning/error messages correctly interpreted by \u2265 95% of clinical users in usability validation per IEC 62366-1:2015+A1:2020",
    standard: "IEC 62366-1:2015+A1:2020; IEC 80601-2-49:2018+AMD1:2024",
  },
  // Additional: Cybersecurity
  {
    no: "10",
    objective: "Cybersecurity and Data Integrity",
    signal: "TPLC Section 6.5: Communication/Transmission Problem (892 reports, 6.7%) includes data integrity failures. Wireless connectivity expansion increases attack surface. Section 6.7.3: Networked monitoring systems face communication failure risks that may also reflect cybersecurity concerns.",
    endpoint: "(a) Unauthorized access attempts to monitoring system; (b) Data corruption events affecting displayed physiological parameters; (c) Network intrusion detection and response time",
    criterion: "(a) Zero successful unauthorized access events; (b) Zero data corruption events affecting clinical decisions; (c) Intrusion detection response \u2264 60 seconds; compliance with IEC 81001-5-1:2021 (health software cybersecurity)",
    standard: "IEC 81001-5-1:2021; FDA Cybersecurity Guidance for Medical Device Manufacturers (2023); EU MDCG 2019-11",
  },
];

// Build Table 5-4
const colW = [500, 2200, 2800, 2400, 1460];
const tableWidth = colW.reduce((a, b) => a + b, 0);

const tableRows = [
  new TableRow({ children: [
    hdrCell("No."), hdrCell("Safety objective"), hdrCell("TPLC safety signal (data source)"), hdrCell("Measurable endpoints"), hdrCell("Acceptance criterion"),
  ]}),
];

for (const ep of safetyEndpoints) {
  tableRows.push(new TableRow({ children: [
    dataCell(ep.no),
    dataCell(ep.objective),
    dataCell(ep.signal),
    dataCell(ep.endpoint),
    dataCell(ep.criterion),
  ]}));
}

children.push(new Table({
  width: { size: tableWidth, type: WidthType.DXA },
  columnWidths: colW,
  rows: tableRows,
}));

children.push(plainPara(""));

// Reference Standards Table
children.push(plainPara("The acceptance criteria and measurable endpoints in Table 5-4 reference the following international standards and published literature:"));

const refStandards = [
  { no: "1", ref: "IEC 60601-1:2005+AMD2:2020", title: "Medical electrical equipment \u2014 Part 1: General requirements for basic safety and essential performance", applicable: "Electrical safety (No. 8), Power supply (No. 7)" },
  { no: "2", ref: "IEC 60601-1-8:2006+AMD2:2020", title: "Medical electrical equipment \u2014 Part 1-8: General requirements, tests and guidance for alarm systems in ME equipment", applicable: "Alarm reliability (No. 1), Alarm fatigue (No. 2), Visual feedback (No. 4)" },
  { no: "3", ref: "IEC 80601-2-49:2018+AMD1:2024", title: "Medical electrical equipment \u2014 Part 2-49: Particular requirements for multifunction patient monitors", applicable: "Software stability (No. 3), Display (No. 4), Communication (No. 5), Power (No. 7), Use safety (No. 9)" },
  { no: "4", ref: "IEC 62304:2006+A1:2015", title: "Medical device software \u2014 Software lifecycle processes", applicable: "Software stability (No. 3)" },
  { no: "5", ref: "IEC 62366-1:2015+A1:2020", title: "Medical devices \u2014 Part 1: Application of usability engineering to medical devices", applicable: "User interface safety (No. 9)" },
  { no: "6", ref: "IEC 81001-5-1:2021", title: "Health software \u2014 Part 5-1: Security for health software \u2014 Processes for security risk management", applicable: "Cybersecurity (No. 10)" },
  { no: "7", ref: "ISO 10993-1:2018", title: "Biological evaluation of medical devices \u2014 Part 1: Evaluation and testing within a risk management process", applicable: "Skin integrity (No. 6)" },
  { no: "8", ref: "Joint Commission NPSG.06.01.01", title: "National Patient Safety Goal: Improve the safety of clinical alarm systems (effective July 1, 2014)", applicable: "Alarm fatigue (No. 2)" },
  { no: "9", ref: "Cvach M. (2012)", title: "Monitor alarm fatigue: An integrative review. Biomed Instrum Technol, 46(4):268-277. PMID: 22839984", applicable: "Alarm fatigue benchmark (No. 2)" },
  { no: "10", ref: "Sendelbach S, Funk M. (2013)", title: "Alarm fatigue: A patient safety concern. AACN Adv Crit Care, 24(4):378-386. PMID: 24153215", applicable: "Alarm fatigue evidence (No. 2)" },
  { no: "11", ref: "ECRI Institute", title: "Top 10 Patient Safety Concerns for Healthcare Organizations (annually published 2014\u20132026)", applicable: "Alarm fatigue benchmark (No. 1)" },
  { no: "12", ref: "FDA Guidance", title: "Content of Premarket Submissions for Management of Cybersecurity in Medical Devices (2023)", applicable: "Cybersecurity (No. 10)" },
];

children.push(new Table({
  width: { size: 9360, type: WidthType.AUTO },
  layout: { type: "autofit" },
  rows: [
    new TableRow({ children: [hdrCell("No."), hdrCell("Standard / Reference"), hdrCell("Title"), hdrCell("Applicable Endpoints")] }),
    ...refStandards.map(r => new TableRow({ children: [
      dataCell(r.no), dataCell(r.ref), dataCell(r.title), dataCell(r.applicable),
    ]})),
  ],
}));

children.push(plainPara(""));

// ---- 5.1 Safety Endpoint Justification ----
children.push(sectionHeading("5.1 Safety Endpoint Justification"));
children.push(bodyPara("Each safety objective in Table 5-4 corresponds to a specific safety signal identified in the FDA TPLC post-market surveillance data (Section 6 of the Safety Data Report). The safety endpoints and acceptance criteria are derived from: (a) quantitative TPLC data (MDR report counts, event severity distributions, and temporal trends); (b) applicable international standards with explicit numerical requirements; and (c) published clinical literature with verified citations. The following subsections provide justification for each safety signal."));

children.push(plainPara(""));
children.push(subHeading("5.1.1 Alarm System Reliability (Safety Endpoints No. 1 & No. 2)"));
children.push(bodyPara("Alarm-related issues represent the most critical safety signal identified in the TPLC database, with 4,739 MDR reports (35.4% of all reports) spanning No Audible Alarm (2,393), Defective Alarm (782), Alarm System issues (649), and No Audible Prompt/Feedback (915). These events are associated with the most severe clinical outcomes: 16 deaths and 187 cardiac arrests (Section 6.6.1). The Joint Commission NPSG.06.01.01 (effective July 1, 2014) mandates hospitals to establish alarm system safety as a priority and develop alarm management policies, validating the clinical significance of this signal."));
children.push(bodyPara("The non-actionable alarm rate benchmark of \u2264 150 per bed per 8-hour shift is derived from Cvach (2012, PMID: 22839984), which conducted an integrative review of alarm fatigue literature between 2000 and 2011, and Sendelbach & Funk (2013, PMID: 24153215), which characterized alarm fatigue as a patient safety concern in AACN Advanced Critical Care. The ECRI Institute has consistently ranked clinical alarm hazards among its Top 10 Patient Safety Concerns from 2014 through 2026, reinforcing the ongoing relevance of this signal."));

children.push(plainPara(""));
children.push(subHeading("5.1.2 Software Stability (Safety Endpoint No. 3 & No. 4)"));
children.push(bodyPara("Software-related malfunctions constitute 2,049 MDR reports (15.3%), encompassing application program problems (590), unexpected shutdowns (405), program freezes (388), unintended shutdowns (416), OS failures (128), and computer software problems (122). Section 6.7.2 identifies increasing software complexity, particularly from wireless connectivity and integrated decision support features, as a contributing factor. For a life-supporting device, IEC 62304 Class C classification requires the highest level of software lifecycle rigor, and the acceptance criterion of \u2265 99.9% system availability reflects this classification."));

children.push(plainPara(""));
children.push(subHeading("5.1.3 Communication and Network Integrity (Safety Endpoint No. 5)"));
children.push(bodyPara("Network-related problems total 1,335 MDR reports (10.0%), including communication/transmission issues (892), wireless communication failures (318), and intermittent communication (125). Section 6.7.3 identifies loss of central monitoring capability as a particular risk in general ward settings where nurse-to-patient ratios are higher. The acceptance criteria (data loss \u2264 0.1%, automatic reconnection within 30 seconds) are aligned with IEC 80601-2-49:2018 Clause 201.12.4.101 requirements for data communication integrity."));

children.push(plainPara(""));
children.push(subHeading("5.1.4 Skin Integrity (Safety Endpoint No. 6)"));
children.push(bodyPara("Skin reactions constitute the most common patient injury category in the TPLC data, with 1,944 reports (14.5% of patient injuries). Section 6.6.2 details the distribution: skin inflammation/irritation (1,879), blisters (38), erythema (14), burns (10), and skin discoloration (5). These injuries are associated with prolonged electrode contact and adhesive sensor placement. The acceptance criterion of Grade \u2265 2 skin injury incidence \u2264 0.5% is consistent with ISO 10993-1:2018 biological evaluation framework, which requires biocompatibility risk assessment for all patient-contacting materials."));

children.push(plainPara(""));
children.push(subHeading("5.1.5 Power System Reliability (Safety Endpoint No. 7)"));
children.push(bodyPara("Power system failures account for 895 MDR reports (6.7%), including power problems (285), failure to charge (234), charging problems (167), failure to power up (115), and complete power loss (94). Section 6.7.5 notes that power failures during active monitoring create complete monitoring gaps. The battery runtime criterion (\u2265 30 minutes at full load) and switchover time (\u2264 1 second) are specified in IEC 80601-2-49:2018 essential performance requirements."));

children.push(plainPara(""));
children.push(subHeading("5.1.6 Electrical Safety (Safety Endpoint No. 8)"));
children.push(bodyPara("Patient leakage current limits (Type CF \u2264 10 \u00B5A normal condition, \u2264 50 \u00B5A single fault condition) are specified in IEC 60601-1:2005 Table 3 and constitute mandatory safety requirements for all medical electrical equipment. Type CF (cardiac floating) applied parts are required for ECG and IBP monitoring functions that have direct cardiac proximity, making these limits particularly relevant for multi-parameter patient monitors. Defibrillation protection is specified in IEC 80601-2-49 for applied parts that may be in the defibrillation current path."));

children.push(plainPara(""));
children.push(subHeading("5.1.7 User Interface and Cybersecurity (Safety Endpoints No. 9 & No. 10)"));
children.push(bodyPara("Patient Device Interaction Problems (1,648 reports, 12.3%) and Incorrect Measurement/Unable to Obtain Readings (893 reports, 6.6%) collectively represent a significant use-safety signal. IEC 62366-1:2015+A1:2020 provides the usability engineering framework for minimizing use errors. Cybersecurity requirements are addressed through IEC 81001-5-1:2021 and FDA premarket guidance, reflecting the increasing connectivity of patient monitoring systems and associated data integrity risks."));

children.push(plainPara(""));
children.push(sectionHeading("5.2 Risk-Benefit Assessment Framework"));
children.push(bodyPara("The clinical safety parameters defined in Table 5-4 form the quantitative basis for the risk-benefit assessment required under EU MDR Article 10(3) and Annex I GSPR. Each parameter includes: (a) a measurable clinical endpoint traceable to a specific TPLC safety signal; (b) an objective acceptance criterion derived from applicable standards, published clinical literature with verified citations, or industry benchmarks; and (c) explicit reference to the TPLC data source (Section 6, subsection numbers) enabling direct traceability."));
children.push(bodyPara("The risk-benefit profile is considered favorable when all safety endpoints meet their acceptance criteria under intended use conditions. The residual risks identified in the TPLC data (alarm fatigue, software instability, communication failures, skin injuries, and power system reliability) are well-characterized and adequately controlled through the measures defined in the risk management file (ISO 14971:2019). The 10 safety endpoints provide a structured framework for ongoing PMCF evaluation and periodic safety update reporting."));

// ===== Build document =====
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4 matching step_06
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children,
  }],
});

const outputPath = "C:\\Users\\ThinkBook\\WorkBuddy\\2026-05-19-task-26\\Clinical_Safety_Parameters_Table_5-4.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("Document created: " + outputPath);
}).catch(err => {
  console.error("Error:", err);
});
