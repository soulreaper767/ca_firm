import frappe
from frappe.utils import today, date_diff


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Finding", "fieldname": "name", "fieldtype": "Link", "options": "QCR Finding", "width": 130},
		{"label": "QCR Review", "fieldname": "qcr_review", "fieldtype": "Link", "options": "QCR Review", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Finding Area", "fieldname": "finding_area", "fieldtype": "Data", "width": 200},
		{"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 130},
		{"label": "Responsible Partner", "fieldname": "responsible_partner", "fieldtype": "Link", "options": "Staff Member", "width": 150},
		{"label": "Target Date", "fieldname": "target_date", "fieldtype": "Date", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Overdue (Days)", "fieldname": "overdue_days", "fieldtype": "Int", "width": 110},
	]


def get_data(filters):
	conditions = {}
	for field in ("qcr_review", "severity", "status", "responsible_partner"):
		if filters.get(field):
			conditions[field] = filters[field]

	rows = frappe.get_all(
		"QCR Finding",
		filters=conditions,
		fields=[
			"name", "qcr_review", "engagement", "finding_area", "severity",
			"responsible_partner", "target_date", "status",
		],
		order_by="field(severity, 'Significant Deficiency', 'Major', 'Minor')",
	)
	for row in rows:
		if row.target_date and row.status != "Closed" and date_diff(today(), row.target_date) > 0:
			row["overdue_days"] = date_diff(today(), row.target_date)
		else:
			row["overdue_days"] = 0
	return rows
