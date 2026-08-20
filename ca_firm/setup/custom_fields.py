import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

CUSTOM_FIELDS = {
	"Company": [
		{
			"fieldname": "ca_firm_section",
			"label": "CA Firm Details",
			"fieldtype": "Section Break",
			"insert_after": "date_of_establishment",
			"collapsible": 1,
		},
		{"fieldname": "strn", "label": "Firm STRN", "fieldtype": "Data", "insert_after": "ca_firm_section"},
		{"fieldname": "icap_firm_category", "label": "ICAP Firm Category", "fieldtype": "Select",
		 "options": "Category A\nCategory B\nCategory C\nCategory D", "insert_after": "strn"},
		{"fieldname": "ca_firm_cb1", "fieldtype": "Column Break", "insert_after": "icap_firm_category"},
		{"fieldname": "default_materiality_benchmark", "label": "Default Materiality Benchmark",
		 "fieldtype": "Select",
		 "options": "Total Revenue\nProfit Before Tax\nTotal Assets\nTotal Equity\nTotal Expenses\n"
		            "Net Profit\nGross Profit\nOther",
		 "insert_after": "ca_firm_cb1"},
		{"fieldname": "enable_time_budget_alerts", "label": "Enable Time Budget Alerts", "fieldtype": "Check",
		 "default": "1", "insert_after": "default_materiality_benchmark"},
		{"fieldname": "time_budget_alert_threshold_percent", "label": "Time Budget Alert Threshold %",
		 "fieldtype": "Percent", "default": "90", "insert_after": "enable_time_budget_alerts"},
		{"fieldname": "engagement_letter_terms", "label": "Standard Engagement Letter Terms",
		 "fieldtype": "Text Editor", "insert_after": "time_budget_alert_threshold_percent"},
	],
	"Customer": [
		{
			"fieldname": "ca_firm_section",
			"label": "Audit Client Profile",
			"fieldtype": "Section Break",
			"insert_after": "customer_details",
			"collapsible": 1,
		},
		{"fieldname": "entity_type", "label": "Entity Type", "fieldtype": "Link", "options": "Entity Type",
		 "insert_after": "ca_firm_section", "in_standard_filter": 1},
		{"fieldname": "entity_size_category", "label": "Entity Size Category (SECP Classification)",
		 "fieldtype": "Link", "options": "Entity Size Category", "insert_after": "entity_type"},
		{"fieldname": "ca_firm_cb1", "fieldtype": "Column Break", "insert_after": "entity_size_category"},
		{"fieldname": "client_relationship_status", "label": "Client Relationship Status", "fieldtype": "Link",
		 "options": "Client Relationship Status", "default": "Prospect", "insert_after": "ca_firm_cb1"},
		{"fieldname": "is_listed_entity", "label": "Listed Entity", "fieldtype": "Check",
		 "insert_after": "client_relationship_status"},
		{"fieldname": "is_public_interest_entity", "label": "Public Interest Entity (PIE)", "fieldtype": "Check",
		 "insert_after": "is_listed_entity"},
		{"fieldname": "ca_firm_section2", "label": "Statutory & Engagement Details", "fieldtype": "Section Break",
		 "insert_after": "is_public_interest_entity", "collapsible": 1},
		{"fieldname": "cuin", "label": "CUIN (SECP Incorporation No)", "fieldtype": "Data",
		 "insert_after": "ca_firm_section2"},
		{"fieldname": "date_of_incorporation", "label": "Date of Incorporation", "fieldtype": "Date",
		 "insert_after": "cuin"},
		{"fieldname": "financial_year_end", "label": "Financial Year End", "fieldtype": "Select",
		 "options": "30 June\n31 December\n31 March\nOther", "default": "30 June",
		 "insert_after": "date_of_incorporation"},
		{"fieldname": "ca_firm_cb2", "fieldtype": "Column Break", "insert_after": "financial_year_end"},
		{"fieldname": "previous_auditor", "label": "Previous Auditor", "fieldtype": "Data",
		 "insert_after": "ca_firm_cb2"},
		{"fieldname": "previous_auditor_removed_reason", "label": "Reason for Change of Auditor (if any)",
		 "fieldtype": "Small Text", "insert_after": "previous_auditor"},
		{"fieldname": "engagement_partner", "label": "Engagement Partner", "fieldtype": "Link",
		 "options": "Employee", "insert_after": "previous_auditor_removed_reason"},
		{"fieldname": "relationship_manager", "label": "Relationship Manager", "fieldtype": "Link",
		 "options": "Employee", "insert_after": "engagement_partner"},
	],
	"Designation": [
		{"fieldname": "designation_level", "label": "Designation Level", "fieldtype": "Int",
		 "insert_after": "description",
		 "description": "1 = Partner ... 7 = Article Assistant (lower is more senior)"},
		{"fieldname": "can_sign_reports", "label": "Can Sign Reports", "fieldtype": "Check",
		 "insert_after": "designation_level"},
		{"fieldname": "can_review", "label": "Can Review", "fieldtype": "Check", "insert_after": "can_sign_reports"},
		{"fieldname": "default_role", "label": "Default Role", "fieldtype": "Link", "options": "Role",
		 "insert_after": "can_review"},
	],
	"Employee": [
		{
			"fieldname": "ca_firm_section",
			"label": "CA Firm Details",
			"fieldtype": "Section Break",
			"insert_after": "designation",
			"collapsible": 1,
		},
		{"fieldname": "icap_membership_no", "label": "ICAP Membership No", "fieldtype": "Data",
		 "insert_after": "ca_firm_section"},
		{"fieldname": "signing_authority", "label": "Signing Authority", "fieldtype": "Check",
		 "insert_after": "icap_membership_no"},
		{"fieldname": "ca_firm_cb1", "fieldtype": "Column Break", "insert_after": "signing_authority"},
		{"fieldname": "chargeable_rate_per_hour", "label": "Chargeable Rate per Hour", "fieldtype": "Currency",
		 "insert_after": "ca_firm_cb1"},
		{"fieldname": "cost_rate_per_hour", "label": "Cost Rate per Hour", "fieldtype": "Currency",
		 "insert_after": "chargeable_rate_per_hour"},
	],
}


def create_all():
	try:
		create_custom_fields(CUSTOM_FIELDS, ignore_validate=True, update=True)
	except Exception:
		frappe.log_error(title="CA Firm: failed to create custom fields")
