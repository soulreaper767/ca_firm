import frappe


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Data", "width": 110},
		{"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Job Incharge", "fieldname": "job_incharge", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Overall Risk", "fieldname": "overall_audit_risk", "fieldtype": "Data", "width": 100},
		{"label": "Target Completion", "fieldname": "target_completion_date", "fieldtype": "Date", "width": 120},
	]
	conditions = {}
	for field in ("client", "status", "engagement_partner", "financial_year"):
		if filters.get(field):
			conditions[field] = filters[field]
	data = frappe.get_all(
		"Statutory Audit Engagement", filters=conditions,
		fields=["name", "client", "financial_year", "engagement_partner", "job_incharge",
		        "status", "overall_audit_risk", "target_completion_date"],
		order_by="modified desc",
	)
	return columns, data
