DESIGNATIONS = [
    {'can_review': 1, 'can_sign_reports': 1, 'designation_level': 1, 'designation_name': 'Partner'},
    {'can_review': 1, 'can_sign_reports': 1, 'designation_level': 1, 'designation_name': 'EQCR Partner'},
    {'can_review': 1, 'can_sign_reports': 0, 'designation_level': 2, 'designation_name': 'Manager'},
    {'can_review': 1, 'can_sign_reports': 0, 'designation_level': 3, 'designation_name': 'Job Incharge'},
    {'can_review': 1, 'can_sign_reports': 0, 'designation_level': 4, 'designation_name': 'Supervisor'},
    {'can_review': 0, 'can_sign_reports': 0, 'designation_level': 5, 'designation_name': 'Senior'},
    {'can_review': 0, 'can_sign_reports': 0, 'designation_level': 6, 'designation_name': 'Semi Senior'},
    {'can_review': 0, 'can_sign_reports': 0, 'designation_level': 7, 'designation_name': 'Article Assistant'},
    {'can_review': 0, 'can_sign_reports': 0, 'designation_level': 7, 'designation_name': 'Paid Assistant'},
]

SIMPLE_MASTERS = {
    "Entity Type": [
        "Private Limited Company", "Public Limited Company (Unlisted)",
        "Public Limited Company (Listed)", "Single Member Company",
        "Company Limited by Guarantee", "Not-for-Profit Company (Section 42)",
        "Limited Liability Partnership", "Partnership Firm", "Sole Proprietorship",
        "Trust", "Society", "Branch Office of Foreign Company", "NGO / NPO",
        "Individual", "Government Entity",
    ],
    "Entity Size Category": [
        "Public Interest Company", "Large-Sized Company", "Medium-Sized Company", "Small-Sized Company",
    ],
    "Client Relationship Status": ["Prospect", "Active", "Inactive", "Terminated"],
    "Engagement Type": [
        "Statutory Audit", "Tax Audit", "Internal Audit", "Limited Review", "Certification",
        "Inventory Audit", "Merger and Acquisition Advisory", "Company Secretarial Services",
        "Bookkeeping and Accounting", "Other",
    ],
    "Billing Frequency": ["One-Time", "Per Engagement", "Monthly", "Quarterly", "Semi-Annually", "Annually"],
    "Fee Arrangement Status": ["Active", "Under Renegotiation", "Lapsed", "Terminated"],
    "Financial Year End Pattern": ["30 June", "31 December", "31 March", "Other"],
    "Revision Type": [
        "Materiality Revised - Down (More Conservative)", "Materiality Revised - Up",
        "Sample Extended - Exceptions Exceeded Tolerable Rate", "Additional Procedures Added",
        "Risk Assessment Revised", "Audit Program Modified", "Scope Expanded",
        "Fraud Risk Identified", "Other",
    ],
    "Permanent File Category": [
        "Incorporation Documents (CTC, Certificate of Incorporation)", "Memorandum and Articles of Association",
        "Shareholding Pattern / Register of Members", "Board Composition and Key Management Contacts",
        "Statutory Registers (Form A/29, Charge Registration)", "Significant Accounting Policies",
        "Organisation Chart", "IT Environment and Systems Overview", "Related Party Structure",
        "Group Structure Chart", "Standing Loan/Facility Agreements", "Other",
    ],
    "Group Relationship Type": ["Subsidiary", "Associate", "Joint Venture", "Branch"],
    "Component Significance": ["Significant Component", "Non-Significant Component"],
    "Consolidation Elimination Type": [
        "Intercompany Sales / Purchases", "Intercompany Receivables / Payables",
        "Unrealized Profit in Intercompany Inventory", "Investment in Subsidiary Elimination",
        "Goodwill on Consolidation", "Non-Controlling Interest", "Other",
    ],
    "Tax Return Type": [
        "Income Tax Return", "Sales Tax Return - Monthly", "Withholding Statement",
        "Wealth Statement", "Advance Tax Estimate", "Other",
    ],
    "Certificate Type": [
        "Turnover Certificate", "Net Worth Certificate", "Stock Statement Certificate",
        "Debtors / Creditors Certificate", "Solvency Certificate", "Other",
    ],
    "Statutory Filing Type": [
        "Annual Return (Form A/29)", "Return of Allotment (Form 3)", "Special Resolution (Form 45)",
        "Change in Directors", "Change in Registered Office", "Board Meeting Minutes",
        "AGM Minutes", "Other",
    ],
    "Bookkeeping Task Type": [
        "Bank Reconciliation", "Sales Tax Return Preparation", "Payroll Processing",
        "Monthly Management Accounts", "Quarterly Financial Statements", "Fixed Asset Register Update",
        "Other",
    ],
    "Tax Notice Type": [
        "Show Cause Notice", "Assessment Order", "Audit Notice", "Penalty Notice",
        "Refund Order", "Notice for Information / Documents", "Recovery Notice", "Other",
    ],
    "Cross Reference Type": [
        "Raises Audit Adjustment", "References Audit Finding", "Shares Financial Head",
        "Escalation", "Depends On", "Supersedes", "Other",
    ],
    "Rating Scale": ["Low", "Medium", "High", "Critical"],
    "Priority Level": ["Low", "Medium", "High", "Urgent"],
    "Concern Level": ["Low Concern", "Medium Concern", "High Concern"],
    "Finding Category": [
        "Control Deficiency", "Compliance Issue", "Accounting Error", "Fraud Indicator",
        "Disclosure Gap", "Other",
    ],
    "Deliverable Type": [
        "Audit Report", "Management Letter", "Statutory Reporting Annexure",
        "Financial Statements", "Other",
    ],
    "Checklist Category": [
        "Client Onboarding", "Engagement Acceptance", "Engagement Completion",
        "Statutory Compliance", "PBC - Documents Required", "Quality Review",
        "Financial Statement Disclosure", "Other",
    ],
    "CAAT Test Category": [
        "Duplicate Detection", "Sequence Gap Test", "Benford's Law", "Round Sum Test",
        "Three-Way Match", "Journal Entry Testing", "Outlier Detection",
        "Segregation of Duties", "Other",
    ],
    "Confirmation Type": [
        "Bank Balance", "Trade Receivable", "Trade Payable", "Legal Confirmation from Lawyer",
        "Investment", "Loan", "Other",
    ],
    "Sampling Method": [
        "Statistical - Random", "Statistical - Monetary Unit Sampling", "Systematic",
        "Judgmental", "Haphazard",
    ],
    "Analysis Type": ["Trend Analysis", "Ratio Analysis", "Reasonableness Test", "Regression Analysis"],
    "Verification Type": ["Fixed Assets", "Inventory", "Cash"],
    "Procedure Stage": ["Planning", "Substantive", "Final Review"],
    "Opinion Type": ["Unmodified", "Qualified", "Adverse", "Disclaimer"],
    "Report Paragraph Type": [
        "Opinion - Unmodified", "Opinion - Qualified", "Opinion - Adverse", "Opinion - Disclaimer",
        "Basis for Opinion", "Basis for Qualified Opinion", "Basis for Adverse Opinion",
        "Basis for Disclaimer of Opinion", "Emphasis of Matter",
        "Material Uncertainty Related to Going Concern", "Other Matter", "Key Audit Matters Introduction",
        "Responsibilities of Management", "Responsibilities of Auditor",
        "Other Reporting Requirements (Fourth Schedule)",
    ],
    "Audit Tick Mark": [
        "Agreed to supporting document", "Agreed to general ledger", "Traced to bank statement",
        "Recalculated / footed", "Confirmed with third party", "Cross-referenced to working paper",
        "Vouched to invoice", "Traced to prior year working papers", "Not an exception",
    ],
    "Component Auditor Role": ["Not Applicable", "We are the Group Auditor", "We are the Component Auditor"],
}

AUDIT_STANDARDS = [
    ("ISA 200", "Overall Objectives of the Independent Auditor", "Standard on Auditing"),
    ("ISA 210", "Agreeing the Terms of Audit Engagements", "Standard on Auditing"),
    ("ISA 220 (Revised)", "Quality Management for an Audit of Financial Statements", "Standard on Auditing"),
    ("ISA 230", "Audit Documentation", "Standard on Auditing"),
    ("ISA 240", "The Auditor's Responsibilities Relating to Fraud", "Standard on Auditing"),
    ("ISA 250", "Consideration of Laws and Regulations", "Standard on Auditing"),
    ("ISA 260", "Communication with Those Charged with Governance", "Standard on Auditing"),
    ("ISA 265", "Communicating Deficiencies in Internal Control", "Standard on Auditing"),
    ("ISA 300", "Planning an Audit of Financial Statements", "Standard on Auditing"),
    ("ISA 315 (Revised)", "Identifying and Assessing the Risks of Material Misstatement", "Standard on Auditing"),
    ("ISA 320", "Materiality in Planning and Performing an Audit", "Standard on Auditing"),
    ("ISA 330", "The Auditor's Responses to Assessed Risks", "Standard on Auditing"),
    ("ISA 402", "Audit Considerations Relating to an Entity Using a Service Organization", "Standard on Auditing"),
    ("ISA 450", "Evaluation of Misstatements Identified during the Audit", "Standard on Auditing"),
    ("ISA 500", "Audit Evidence", "Standard on Auditing"),
    ("ISA 501", "Audit Evidence - Specific Considerations for Selected Items", "Standard on Auditing"),
    ("ISA 505", "External Confirmations", "Standard on Auditing"),
    ("ISA 510", "Initial Audit Engagements - Opening Balances", "Standard on Auditing"),
    ("ISA 520", "Analytical Procedures", "Standard on Auditing"),
    ("ISA 530", "Audit Sampling", "Standard on Auditing"),
    ("ISA 540 (Revised)", "Auditing Accounting Estimates", "Standard on Auditing"),
    ("ISA 550", "Related Parties", "Standard on Auditing"),
    ("ISA 560", "Subsequent Events", "Standard on Auditing"),
    ("ISA 570 (Revised)", "Going Concern", "Standard on Auditing"),
    ("ISA 580", "Written Representations", "Standard on Auditing"),
    ("ISA 600 (Revised)", "Special Considerations - Group Audits", "Standard on Auditing"),
    ("ISA 610 (Revised)", "Using the Work of Internal Auditors", "Standard on Auditing"),
    ("ISA 620", "Using the Work of an Auditor's Expert", "Standard on Auditing"),
    ("ISA 700 (Revised)", "Forming an Opinion and Reporting on Financial Statements", "Standard on Auditing"),
    ("ISA 701", "Communicating Key Audit Matters", "Standard on Auditing"),
    ("ISA 705 (Revised)", "Modifications to the Opinion", "Standard on Auditing"),
    ("ISA 706 (Revised)", "Emphasis of Matter and Other Matter Paragraphs", "Standard on Auditing"),
    ("ISA 710", "Comparative Information", "Standard on Auditing"),
    ("ISA 720 (Revised)", "The Auditor's Responsibilities Relating to Other Information", "Standard on Auditing"),
    ("ISQM 1", "Quality Management for Firms that Perform Audits or Reviews of Financial Statements",
     "Standard on Quality Control"),
    ("ISQM 2", "Engagement Quality Reviews", "Standard on Quality Control"),
    ("ISRE 2400 (Revised)", "Engagements to Review Historical Financial Statements",
     "Standard on Review Engagements"),
]

FS_AREAS = [
    ("Revenue", "Profit and Loss", "High"),
    ("Purchases and Expenses", "Profit and Loss", "Medium"),
    ("Property, Plant and Equipment", "Balance Sheet", "Medium"),
    ("Intangible Assets", "Balance Sheet", "Medium"),
    ("Inventory", "Balance Sheet", "High"),
    ("Cash and Bank Balances", "Balance Sheet", "Medium"),
    ("Trade Receivables", "Balance Sheet", "High"),
    ("Trade Payables", "Balance Sheet", "Medium"),
    ("Loans and Borrowings", "Balance Sheet", "Medium"),
    ("Provisions and Contingent Liabilities", "Balance Sheet", "High"),
    ("Employee Benefits and Payroll", "Both", "Medium"),
    ("Related Party Transactions", "Both", "High"),
    ("Equity and Reserves", "Balance Sheet", "Low"),
    ("Investments", "Balance Sheet", "Medium"),
    ("Taxation - Current and Deferred", "Both", "High"),
    ("Other Income and Other Expenses", "Profit and Loss", "Low"),
]

ASSERTIONS = [
    ("Existence", "Account Balances"),
    ("Completeness", "Account Balances"),
    ("Rights and Obligations", "Account Balances"),
    ("Accuracy, Valuation and Allocation", "Account Balances"),
    ("Occurrence", "Classes of Transactions and Events"),
    ("Cut-off", "Classes of Transactions and Events"),
    ("Classification", "Classes of Transactions and Events"),
    ("Presentation", "Presentation and Disclosure"),
]

RISK_CATEGORIES = [
    ("Management Override of Controls", "Fraud"),
    ("Revenue Recognition", "Fraud"),
    ("Complex or Unusual Transactions", "Inherent"),
    ("Significant Accounting Estimates", "Inherent"),
    ("IT General Controls Weakness", "Control"),
    ("Related Party Transactions", "Inherent"),
    ("Going Concern", "Business"),
    ("Regulatory Non-Compliance", "Business"),
]

APPLICABLE_LAWS = [
    "Companies Act, 2017", "Income Tax Ordinance, 2001", "Sales Tax Act, 1990",
    "Federal Excise Act, 2005", "Foreign Exchange Regulation Act, 1947 (SBP Regulations)",
    "Anti-Money Laundering Act, 2010", "SECP Code of Corporate Governance Regulations, 2019",
    "SECP Companies (Accounting and Auditing Standards) Rules, 2015",
    "International Financial Reporting Standards (IFRS) as adopted in Pakistan",
    "Fourth Schedule to the Companies Act, 2017 (Auditor's Report)",
    "Fifth Schedule to the Companies Act, 2017 (Financial Statement Disclosures)",
]

PROCEDURE_TYPES = [
    "Inquiry", "Observation", "Inspection of Records or Documents", "Inspection of Tangible Assets",
    "Recalculation", "Reperformance", "External Confirmation", "Analytical Procedure",
    "Test of Control", "Computer Assisted Audit Technique (CAAT)",
]

CAAT_TEMPLATES = [
    ("Duplicate Invoice / Payment Detection", "Duplicate Detection", "Trade Payables"),
    ("Invoice Sequence Gap Test", "Sequence Gap Test", "Revenue"),
    ("Benford's Law Analysis on GL Entries", "Benford's Law", None),
    ("Round Sum Journal Entry Test", "Round Sum Test", None),
    ("Three-Way Match - PO, GRN, Invoice", "Three-Way Match", "Purchases and Expenses"),
    ("Journal Entries Posted by Unauthorized Users", "Journal Entry Testing", None),
    ("Journal Entries Posted on Weekends/Holidays", "Journal Entry Testing", None),
    ("Outlier Detection on Expense Accounts", "Outlier Detection", "Purchases and Expenses"),
    ("Segregation of Duties Conflict Report", "Segregation of Duties", None),
]

# (template_name, category, [(item_no, particular, is_mandatory, entity_size, listed_only, pie_only, industry), ...])
CHECKLIST_TEMPLATES = [
    {
        "template_name": "Engagement Acceptance Checklist",
        "category": "Engagement Acceptance",
        "items": [
            (1, "Preliminary independence and conflict-of-interest check completed", 1, None, False, False, None),
            (2, "Client integrity assessment completed (management, ownership, business reputation)", 1, None, False, False, None),
            (3, "Competence to perform the engagement confirmed (skills, resources, industry knowledge)", 1, None, False, False, None),
            (4, "Communication with predecessor auditor completed (if applicable) and NOC obtained", 1, None, False, False, None),
            (5, "Preliminary assessment of applicable financial reporting framework completed", 1, None, False, False, None),
            (6, "Engagement letter drafted and terms agreed with those charged with governance", 1, None, False, False, None),
            (7, "Fee arrangement agreed and documented", 1, None, False, False, None),
            (8, "Additional AML customer due diligence completed for DNFBP-category client", 0, None, False, False, None),
        ],
    },
    {
        "template_name": "PBC - Documents Required Checklist",
        "category": "PBC - Documents Required",
        "items": [
            (1, "Trial balance and general ledger for the year", 1, None, False, False, None),
            (2, "Prior year audited financial statements", 1, None, False, False, None),
            (3, "Bank statements and bank reconciliations for all accounts", 1, None, False, False, None),
            (4, "Fixed asset register with additions/disposals during the year", 1, None, False, False, None),
            (5, "Inventory count sheets and costing records", 1, None, False, False, None),
            (6, "Debtors and creditors ageing schedules", 1, None, False, False, None),
            (7, "Loan agreements and confirmations", 1, None, False, False, None),
            (8, "Board/shareholder minutes for the year", 1, None, False, False, None),
            (9, "Statutory registers (SECP Form A/29, share register)", 1, None, False, False, None),
            (10, "Related party transaction schedule", 1, None, False, False, None),
            (11, "Corporate Governance compliance statement and Board Audit Committee minutes", 1, None, True, False, None),
            (12, "Related party disclosures reconciled to Fourth/Fifth Schedule format", 1, None, False, True, None),
        ],
    },
    {
        "template_name": "Financial Statement Disclosure Checklist",
        "category": "Financial Statement Disclosure",
        "items": [
            (1, "Statement of financial position presented in classified format", 1, None, False, False, None),
            (2, "Statement of profit or loss and other comprehensive income presented", 1, None, False, False, None),
            (3, "Statement of changes in equity presented", 1, None, False, False, None),
            (4, "Statement of cash flows presented (direct or indirect method)", 1, None, False, False, None),
            (5, "Summary of significant accounting policies disclosed", 1, None, False, False, None),
            (6, "Related party transactions and balances disclosed per IAS 24", 1, None, False, False, None),
            (7, "Full Fourth/Fifth Schedule disclosure set applied (no reduced disclosure)", 1, "Large-Sized Company", False, False, None),
            (8, "Full Fourth/Fifth Schedule disclosure set applied (no reduced disclosure)", 1, "Public Interest Company", False, False, None),
            (9, "Reduced disclosure under AFRS for Small-Sized Entities applied", 1, "Small-Sized Company", False, False, None),
            (10, "Corporate Governance compliance disclosures included (Regulation 36)", 1, None, True, False, None),
            (11, "Earnings per share disclosure per IAS 33", 1, None, True, False, None),
            (12, "Segment reporting disclosure per IFRS 8", 0, None, False, True, None),
        ],
    },
    {
        "template_name": "Engagement Completion Checklist",
        "category": "Engagement Completion",
        "items": [
            (1, "All planned audit procedures completed and cross-referenced to working papers", 1, None, False, False, None),
            (2, "All review notes cleared", 1, None, False, False, None),
            (3, "Subsequent events review performed up to the date of the auditor's report", 1, None, False, False, None),
            (4, "Written representations obtained from management and signed", 1, None, False, False, None),
            (5, "Going concern assessment concluded", 1, None, False, False, None),
            (6, "Summary of uncorrected misstatements evaluated against materiality", 1, None, False, False, None),
            (7, "Engagement Quality Control Review completed and matters cleared", 1, "Public Interest Company", False, False, None),
            (8, "Key Audit Matters identified and documented", 1, None, True, False, None),
            (9, "Management letter drafted and points cleared with management", 1, None, False, False, None),
            (10, "Audit report drafted, reviewed and approved by the engagement partner", 1, None, False, False, None),
        ],
    },
]

# (template_name, fs_area, [(step_desc, assertion, procedure_type, is_caat), ...])
AUDIT_PROGRAM_TEMPLATES = [
    {
        "template_name": "Revenue - Standard Audit Program",
        "fs_area": "Revenue",
        "steps": [
            ("Obtain and review revenue recognition policy for compliance with IFRS 15", "Presentation", "Inspection of Records or Documents", 0),
            ("Perform analytical review of revenue by month/product/customer against expectation", "Occurrence", "Analytical Procedure", 0),
            ("Test a sample of sales transactions to supporting documentation (order, dispatch, invoice)", "Occurrence", "Inspection of Records or Documents", 0),
            ("Perform cut-off testing around year-end for sales and returns", "Cut-off", "Inspection of Records or Documents", 0),
            ("Run CAAT: sales invoice sequence gap test", "Completeness", "Computer Assisted Audit Technique (CAAT)", 1),
            ("Confirm significant customer balances directly", "Existence", "External Confirmation", 0),
            ("Test journal entries affecting revenue for unusual postings", "Occurrence", "Computer Assisted Audit Technique (CAAT)", 1),
        ],
    },
    {
        "template_name": "Trade Receivables - Standard Audit Program",
        "fs_area": "Trade Receivables",
        "steps": [
            ("Obtain debtors ageing and agree control total to general ledger", "Completeness", "Recalculation", 0),
            ("Select sample and send external confirmations to debtors", "Existence", "External Confirmation", 0),
            ("Perform alternative procedures for non-responses (subsequent receipts, invoices)", "Existence", "Inspection of Records or Documents", 0),
            ("Review ageing for indicators of impairment and assess provisioning adequacy", "Accuracy, Valuation and Allocation", "Analytical Procedure", 0),
            ("Test subsequent cash receipts after year-end", "Existence", "Inspection of Records or Documents", 0),
            ("Review for related party receivables and appropriate disclosure", "Presentation", "Inspection of Records or Documents", 0),
        ],
    },
    {
        "template_name": "Property, Plant and Equipment - Standard Audit Program",
        "fs_area": "Property, Plant and Equipment",
        "steps": [
            ("Obtain fixed asset register and agree opening balances to prior year", "Completeness", "Recalculation", 0),
            ("Vouch a sample of additions to invoices/agreements", "Existence", "Inspection of Records or Documents", 0),
            ("Verify disposals and recompute gain/loss on disposal", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Physically inspect a sample of significant assets", "Existence", "Inspection of Tangible Assets", 0),
            ("Recalculate depreciation charge and compare to policy/useful lives", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Assess indicators of impairment under IAS 36", "Accuracy, Valuation and Allocation", "Inquiry", 0),
            ("Confirm title/ownership for a sample of significant assets (registration documents)", "Rights and Obligations", "Inspection of Records or Documents", 0),
        ],
    },
    {
        "template_name": "Inventory - Standard Audit Program",
        "fs_area": "Inventory",
        "steps": [
            ("Attend physical inventory count and perform test counts", "Existence", "Observation", 0),
            ("Reconcile physical count results to perpetual/book records", "Completeness", "Recalculation", 0),
            ("Test costing (raw material, WIP, finished goods) for a sample of items", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Assess net realizable value and review for slow-moving/obsolete stock", "Accuracy, Valuation and Allocation", "Analytical Procedure", 0),
            ("Test cut-off of goods received/dispatched around year-end and count date", "Cut-off", "Inspection of Records or Documents", 0),
            ("Review for consigned/third-party inventory and confirm ownership", "Rights and Obligations", "External Confirmation", 0),
        ],
    },
    {
        "template_name": "Trade Payables - Standard Audit Program",
        "fs_area": "Trade Payables",
        "steps": [
            ("Obtain creditors listing and agree control total to general ledger", "Completeness", "Recalculation", 0),
            ("Perform search for unrecorded liabilities (subsequent payments/invoices)", "Completeness", "Inspection of Records or Documents", 0),
            ("Select sample and request supplier statement/confirmation", "Existence", "External Confirmation", 0),
            ("Test a sample of payables to supporting invoices/GRNs", "Existence", "Inspection of Records or Documents", 0),
            ("Review for related party payables and disclosure", "Presentation", "Inspection of Records or Documents", 0),
        ],
    },
    {
        "template_name": "Cash and Bank - Standard Audit Program",
        "fs_area": "Cash and Bank Balances",
        "steps": [
            ("Obtain bank confirmations directly from all banks for all accounts held", "Existence", "External Confirmation", 0),
            ("Review bank reconciliations for all accounts and test reconciling items", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Perform cash count for petty cash/cash in hand where material", "Existence", "Observation", 0),
            ("Test for unusual transfers or window-dressing around year-end", "Occurrence", "Analytical Procedure", 0),
        ],
    },
    {
        "template_name": "Taxation - Standard Audit Program",
        "fs_area": "Taxation - Current and Deferred",
        "steps": [
            ("Recompute current tax provision as per Income Tax Ordinance, 2001", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Review deferred tax computation and temporary differences", "Accuracy, Valuation and Allocation", "Recalculation", 0),
            ("Reconcile monthly sales tax returns with books of account", "Completeness", "Reperformance", 0),
            ("Review withholding tax compliance and reconciliation with challans deposited", "Completeness", "Reperformance", 0),
        ],
    },
]

# (title, applicable_law, entity_type, industry, size, listed_only, pie_only, mandatory, description)
REGULATORY_REQUIREMENTS = [
    (
        "Statutory Audit Requirement - Companies Act 2017", "Companies Act, 2017",
        None, None, None, False, False, True,
        "Every company (other than a company qualifying for exemption under SECP thresholds) is "
        "required to have its accounts audited by a chartered accountant in practice.",
    ),
    (
        "Code of Corporate Governance Applicability", "SECP Code of Corporate Governance Regulations, 2019",
        "Public Limited Company (Listed)", None, None, True, False, True,
        "Listed companies are required to comply with the SECP Code of Corporate Governance "
        "Regulations, 2019, including composition of the Board, Audit Committee, and related "
        "disclosures, which the auditor reports on separately.",
    ),
    (
        "Reduced Disclosure - Small-Sized Company", "SECP Companies (Accounting and Auditing Standards) Rules, 2015",
        None, None, "Small-Sized Company", False, False, False,
        "Small-Sized Companies as classified by SECP may apply the Accounting and Financial Reporting "
        "Standard for Small-Sized Entities (AFRS for SSEs) with reduced disclosure requirements.",
    ),
    (
        "Public Interest Company - Full IFRS and EQCR", "SECP Companies (Accounting and Auditing Standards) Rules, 2015",
        None, None, "Public Interest Company", False, True, True,
        "Public Interest Companies must apply full IFRS as notified by SECP and the engagement is "
        "subject to Engagement Quality Control Review (EQCR) under the firm's quality management "
        "system.",
    ),
    (
        "Tax Audit Selection Risk - Section 214C", "Income Tax Ordinance, 2001",
        None, None, None, False, False, False,
        "Every taxpayer is exposed to random computer-ballot selection for audit under section 214C "
        "(or specific selection under section 177). Relevant to the auditor's assessment of tax "
        "contingencies and disclosure of contingent liabilities.",
    ),
]

# (title, paragraph_type, text, is_default)
AUDIT_OPINION_PARAGRAPHS = [
    (
        "Unmodified Opinion - Standard",
        "Opinion - Unmodified",
        "We have audited the annexed financial statements of {{ client_name }} (the Company), which "
        "comprise the statement of financial position as at {{ period_end }}, and the statement of "
        "profit or loss, statement of comprehensive income, statement of changes in equity, statement "
        "of cash flows for the year then ended, and notes to the financial statements, including a "
        "summary of significant accounting policies.\n\nIn our opinion, the accompanying financial "
        "statements give a true and fair view of the state of the Company's affairs as at "
        "{{ period_end }}, and of the profit, comprehensive income, changes in equity, and cash flows "
        "for the year then ended in accordance with {{ framework }}.",
        True,
    ),
    (
        "Basis for Opinion - Standard",
        "Basis for Opinion",
        "We conducted our audit in accordance with International Standards on Auditing (ISAs) as "
        "applicable in Pakistan. Our responsibilities under those standards are further described in "
        "the Auditor's Responsibilities for the Audit of the Financial Statements section of our "
        "report. We are independent of the Company in accordance with the International Ethics "
        "Standards Board for Accountants' Code of Ethics for Professional Accountants as adopted by "
        "ICAP (the Code), and we have fulfilled our other ethical responsibilities in accordance with "
        "the Code. We believe that the audit evidence we have obtained is sufficient and appropriate "
        "to provide a basis for our opinion.",
        True,
    ),
    (
        "Qualified Opinion - Standard",
        "Opinion - Qualified",
        "We have audited the annexed financial statements of {{ client_name }}, which comprise the "
        "statement of financial position as at {{ period_end }}, and the statement of profit or loss, "
        "statement of comprehensive income, statement of changes in equity and statement of cash flows "
        "for the year then ended, and notes to the financial statements, including a summary of "
        "significant accounting policies.\n\nIn our opinion, except for the effects of the matter "
        "described in the Basis for Qualified Opinion section of our report, the accompanying financial "
        "statements give a true and fair view of the state of the Company's affairs as at "
        "{{ period_end }}, and of the profit, comprehensive income, changes in equity and cash flows for "
        "the year then ended in accordance with {{ framework }}.",
        True,
    ),
    (
        "Basis for Qualified Opinion - Misstatement Template",
        "Basis for Qualified Opinion",
        "[Describe the matter giving rise to the qualification - e.g.] As disclosed in note [X] to the "
        "financial statements, [description of departure from the applicable framework and its "
        "financial effect, referencing amounts such as the overall materiality of "
        "{{ overall_materiality }} where relevant].",
        True,
    ),
    (
        "Adverse Opinion - Standard",
        "Opinion - Adverse",
        "We have audited the annexed financial statements of {{ client_name }}...\n\nIn our opinion, "
        "because of the significance of the matter described in the Basis for Adverse Opinion section "
        "of our report, the accompanying financial statements do not give a true and fair view of the "
        "state of the Company's affairs as at {{ period_end }}, and of its profit, comprehensive "
        "income, changes in equity and cash flows for the year then ended, in accordance with "
        "{{ framework }}.",
        True,
    ),
    (
        "Disclaimer of Opinion - Standard",
        "Opinion - Disclaimer",
        "We were engaged to audit the annexed financial statements of {{ client_name }}...\n\nWe do "
        "not express an opinion on the accompanying financial statements of the Company. Because of "
        "the significance of the matter described in the Basis for Disclaimer of Opinion section of "
        "our report, we have not been able to obtain sufficient appropriate audit evidence to provide "
        "a basis for an audit opinion on these financial statements.",
        True,
    ),
    (
        "Material Uncertainty Related to Going Concern - Standard",
        "Material Uncertainty Related to Going Concern",
        "We draw attention to note [X] in the financial statements, which indicates that [describe the "
        "principal conditions or events, individually or collectively, that give rise to significant "
        "doubt on the Company's ability to continue as a going concern]. As stated in note [X], these "
        "events or conditions, along with other matters as set forth in note [X], indicate that a "
        "material uncertainty exists that may cast significant doubt on the Company's ability to "
        "continue as a going concern. Our opinion is not modified in respect of this matter.",
        True,
    ),
    (
        "Responsibilities of Management - Standard",
        "Responsibilities of Management",
        "Management is responsible for the preparation and fair presentation of the financial "
        "statements in accordance with {{ framework }} and the requirements of the Companies Act, "
        "2017 (XIX of 2017), and for such internal control as management determines is necessary to "
        "enable the preparation of financial statements that are free from material misstatement, "
        "whether due to fraud or error.\n\nIn preparing the financial statements, management is "
        "responsible for assessing the Company's ability to continue as a going concern, disclosing, "
        "as applicable, matters related to going concern and using the going concern basis of "
        "accounting unless management either intends to liquidate the Company or to cease operations, "
        "or has no realistic alternative but to do so.\n\nThe Board of Directors is responsible for "
        "overseeing the Company's financial reporting process.",
        True,
    ),
    (
        "Responsibilities of Auditor - Standard",
        "Responsibilities of Auditor",
        "Our objectives are to obtain reasonable assurance about whether the financial statements as a "
        "whole are free from material misstatement, whether due to fraud or error, and to issue an "
        "auditor's report that includes our opinion. Reasonable assurance is a high level of assurance "
        "but is not a guarantee that an audit conducted in accordance with ISAs as applicable in "
        "Pakistan will always detect a material misstatement when it exists. Misstatements can arise "
        "from fraud or error and are considered material if, individually or in the aggregate, they "
        "could reasonably be expected to influence the economic decisions of users taken on the basis "
        "of these financial statements.\n\nAs part of an audit in accordance with ISAs as applicable "
        "in Pakistan, we exercise professional judgment and maintain professional skepticism throughout "
        "the audit. We also identify and assess the risks of material misstatement of the financial "
        "statements, whether due to fraud or error, design and perform audit procedures responsive to "
        "those risks, obtain an understanding of internal control relevant to the audit, evaluate the "
        "appropriateness of accounting policies used and the reasonableness of accounting estimates, "
        "conclude on the appropriateness of management's use of the going concern basis of accounting, "
        "and evaluate the overall presentation, structure and content of the financial statements.",
        True,
    ),
    (
        "Other Reporting Requirements - Fourth Schedule Standard",
        "Other Reporting Requirements (Fourth Schedule)",
        "Based on our audit, we further report that in our opinion:\n\na) proper books of account have "
        "been kept by the Company as required by the Companies Act, 2017 (XIX of 2017);\n\nb) the "
        "statement of financial position, the statement of profit or loss, the statement of "
        "comprehensive income, the statement of changes in equity and the statement of cash flows "
        "together with the notes thereon have been drawn up in conformity with the Companies Act, 2017 "
        "(XIX of 2017), and are in agreement with the books of account;\n\nc) investments made, "
        "expenditure incurred and guarantees extended during the year were for the purpose of the "
        "Company's business; and\n\nd) zakat deductible at source under the Zakat and Ushr Ordinance, "
        "1980 (XVIII of 1980), was deducted by the Company and deposited in the Central Zakat Fund "
        "within the prescribed time (where applicable).",
        True,
    ),
]

# (template_name, opinion_type, [(paragraph_type, paragraph_title, sequence), ...])
AUDIT_REPORT_TEMPLATES = [
    (
        "Standard Unmodified Report", "Unmodified",
        [
            ("Opinion - Unmodified", "Unmodified Opinion - Standard", 10),
            ("Basis for Opinion", "Basis for Opinion - Standard", 20),
            ("Responsibilities of Management", "Responsibilities of Management - Standard", 30),
            ("Responsibilities of Auditor", "Responsibilities of Auditor - Standard", 40),
            ("Other Reporting Requirements (Fourth Schedule)", "Other Reporting Requirements - Fourth Schedule Standard", 50),
        ],
    ),
    (
        "Standard Qualified Report", "Qualified",
        [
            ("Opinion - Qualified", "Qualified Opinion - Standard", 10),
            ("Basis for Qualified Opinion", "Basis for Qualified Opinion - Misstatement Template", 20),
            ("Responsibilities of Management", "Responsibilities of Management - Standard", 30),
            ("Responsibilities of Auditor", "Responsibilities of Auditor - Standard", 40),
            ("Other Reporting Requirements (Fourth Schedule)", "Other Reporting Requirements - Fourth Schedule Standard", 50),
        ],
    ),
]

# (line_item_name, statement_type, classification, parent_line_item, sequence, is_subtotal, fs_area)
FS_LINE_ITEMS = [
    ("Property, Plant and Equipment", "Balance Sheet", "Asset - Non Current", None, 10, False, "Property, Plant and Equipment"),
    ("Intangible Assets", "Balance Sheet", "Asset - Non Current", None, 20, False, "Intangible Assets"),
    ("Long-term Investments", "Balance Sheet", "Asset - Non Current", None, 30, False, "Investments"),
    ("Stock-in-Trade", "Balance Sheet", "Asset - Current", None, 110, False, "Inventory"),
    ("Trade Debts", "Balance Sheet", "Asset - Current", None, 120, False, "Trade Receivables"),
    ("Loans and Advances", "Balance Sheet", "Asset - Current", None, 130, False, None),
    ("Other Receivables", "Balance Sheet", "Asset - Current", None, 140, False, "Trade Receivables"),
    ("Cash and Bank Balances", "Balance Sheet", "Asset - Current", None, 150, False, "Cash and Bank Balances"),
    ("Share Capital", "Balance Sheet", "Equity", None, 210, False, "Equity and Reserves"),
    ("Reserves and Unappropriated Profit", "Balance Sheet", "Equity", None, 220, False, "Equity and Reserves"),
    ("Long-term Borrowings", "Balance Sheet", "Liability - Non Current", None, 310, False, "Loans and Borrowings"),
    ("Deferred Taxation", "Balance Sheet", "Liability - Non Current", None, 320, False, "Taxation - Current and Deferred"),
    ("Trade and Other Payables", "Balance Sheet", "Liability - Current", None, 410, False, "Trade Payables"),
    ("Short-term Borrowings", "Balance Sheet", "Liability - Current", None, 420, False, "Loans and Borrowings"),
    ("Provision for Taxation", "Balance Sheet", "Liability - Current", None, 430, False, "Taxation - Current and Deferred"),
    ("Revenue from Contracts with Customers", "Profit and Loss", "Income", None, 510, False, "Revenue"),
    ("Cost of Sales", "Profit and Loss", "Expense", None, 520, False, "Purchases and Expenses"),
    ("Administrative Expenses", "Profit and Loss", "Expense", None, 530, False, "Purchases and Expenses"),
    ("Other Income and Other Expenses", "Profit and Loss", "Income", None, 540, False, "Other Income and Other Expenses"),
    ("Finance Costs", "Profit and Loss", "Expense", None, 550, False, "Loans and Borrowings"),
    ("Taxation", "Profit and Loss", "Expense", None, 560, False, "Taxation - Current and Deferred"),
]

# (head_name, fs_line_item, fs_area, nature)
COA_HEADS = [
    ("Local Sales", "Revenue from Contracts with Customers", "Revenue", "Credit"),
    ("Export Sales", "Revenue from Contracts with Customers", "Revenue", "Credit"),
    ("Raw Material Consumed", "Cost of Sales", "Purchases and Expenses", "Debit"),
    ("Direct Labour", "Cost of Sales", "Purchases and Expenses", "Debit"),
    ("Salaries, Wages and Benefits - Admin", "Administrative Expenses", "Employee Benefits and Payroll", "Debit"),
    ("Depreciation - Owned Assets", "Administrative Expenses", "Property, Plant and Equipment", "Debit"),
    ("Mark-up on Borrowings", "Finance Costs", "Loans and Borrowings", "Debit"),
    ("Property, Plant and Equipment - Cost", "Property, Plant and Equipment", "Property, Plant and Equipment", "Debit"),
    ("Accumulated Depreciation", "Property, Plant and Equipment", "Property, Plant and Equipment", "Credit"),
    ("Raw Material and Finished Goods Stock", "Stock-in-Trade", "Inventory", "Debit"),
    ("Trade Debtors - Local", "Trade Debts", "Trade Receivables", "Debit"),
    ("Trade Debtors - Export", "Trade Debts", "Trade Receivables", "Debit"),
    ("Cash in Hand", "Cash and Bank Balances", "Cash and Bank Balances", "Debit"),
    ("Bank Accounts - Current", "Cash and Bank Balances", "Cash and Bank Balances", "Debit"),
    ("Trade Creditors", "Trade and Other Payables", "Trade Payables", "Credit"),
    ("Accrued Liabilities", "Trade and Other Payables", "Trade Payables", "Credit"),
    ("Long-term Loan from Bank", "Long-term Borrowings", "Loans and Borrowings", "Credit"),
    ("Running Finance", "Short-term Borrowings", "Loans and Borrowings", "Credit"),
    ("Provision for Taxation - Current Year", "Provision for Taxation", "Taxation - Current and Deferred", "Credit"),
    ("Issued, Subscribed and Paid-up Capital", "Share Capital", "Equity and Reserves", "Credit"),
    ("Unappropriated Profit", "Reserves and Unappropriated Profit", "Equity and Reserves", "Credit"),
]
