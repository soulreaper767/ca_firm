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
}
