import frappe
from frappe.utils import today, date_diff


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Review Note", "fieldname": "name", "fieldtype": "Link", "options": "Review Note", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Raised By", "fieldname": "raised_by", "fieldtype": "Link", "options": "Staff Member", "width": 120},
		{"label": "Raised To", "fieldname": "raised_to", "fieldtype": "Link", "options": "Staff Member", "width": 120},
		{"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 90},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Raised Date", "fieldname": "raised_date", "fieldtype": "Date", "width": 110},
		{"label": "Age (Days)", "fieldname": "age_days", "fieldtype": "Int", "width": 100},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "raised_to", "status", "priority"):
		if filters.get(field):
			conditions[field] = filters[field]

	rows = frappe.get_all(
		"Review Note",
		filters=conditions,
		fields=["name", "engagement", "raised_by", "raised_to", "priority", "status", "raised_date"],
		order_by="raised_date asc",
	)
	for row in rows:
		if row.raised_date and row.status in ("Open", "Reopened"):
			row["age_days"] = date_diff(today(), row.raised_date)
		else:
			row["age_days"] = None
	return rows
