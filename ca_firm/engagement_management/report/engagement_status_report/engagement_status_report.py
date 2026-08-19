import frappe
from frappe.utils import today, date_diff


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 160},
		{"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Data", "width": 110},
		{"label": "Engagement Type", "fieldname": "engagement_type", "fieldtype": "Data", "width": 120},
		{"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Staff Member", "width": 130},
		{"label": "Manager", "fieldname": "engagement_manager", "fieldtype": "Link", "options": "Staff Member", "width": 130},
		{"label": "Job Incharge", "fieldname": "job_incharge", "fieldtype": "Link", "options": "Staff Member", "width": 130},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Risk", "fieldname": "overall_audit_risk", "fieldtype": "Data", "width": 80},
		{"label": "Target Completion", "fieldname": "target_completion_date", "fieldtype": "Date", "width": 130},
		{"label": "Days to/Overdue", "fieldname": "days_remaining", "fieldtype": "Int", "width": 120},
	]


def get_data(filters):
	conditions = {}
	for field in ("client", "status", "engagement_partner", "financial_year"):
		if filters.get(field):
			conditions[field] = filters[field]

	rows = frappe.get_all(
		"Engagement",
		filters=conditions,
		fields=[
			"name", "client", "financial_year", "engagement_type", "engagement_partner",
			"engagement_manager", "job_incharge", "status", "overall_audit_risk", "target_completion_date",
		],
		order_by="target_completion_date asc",
	)
	for row in rows:
		if row.target_completion_date and row.status not in ("Completed", "Archived", "Declined"):
			row["days_remaining"] = date_diff(row.target_completion_date, today())
		else:
			row["days_remaining"] = None
	return rows
