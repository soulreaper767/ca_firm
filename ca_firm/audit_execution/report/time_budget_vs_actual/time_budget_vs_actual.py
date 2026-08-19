import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Procedure", "fieldname": "procedure_description", "fieldtype": "Data", "width": 260},
		{"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Link", "options": "Staff Member", "width": 130},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
		{"label": "Budgeted Hours", "fieldname": "budgeted_hours", "fieldtype": "Float", "width": 120},
		{"label": "Actual Hours", "fieldname": "actual_hours", "fieldtype": "Float", "width": 110},
		{"label": "Variance", "fieldname": "variance", "fieldtype": "Float", "width": 100},
		{"label": "% Utilised", "fieldname": "percent_utilised", "fieldtype": "Percent", "width": 100},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "assigned_to", "status"):
		if filters.get(field):
			conditions[field] = filters[field]

	rows = frappe.get_all(
		"Audit Procedure",
		filters=conditions,
		fields=[
			"engagement", "procedure_description", "assigned_to", "status",
			"budgeted_hours", "actual_hours",
		],
		order_by="engagement asc",
	)
	for row in rows:
		budgeted = row.budgeted_hours or 0
		actual = row.actual_hours or 0
		row["variance"] = actual - budgeted
		row["percent_utilised"] = (actual / budgeted * 100) if budgeted else 0
	return rows
