import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Finding", "fieldname": "name", "fieldtype": "Link", "options": "Audit Finding", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Title", "fieldname": "finding_title", "fieldtype": "Data", "width": 220},
		{"label": "FS Area", "fieldname": "fs_area", "fieldtype": "Link", "options": "Financial Statement Area", "width": 160},
		{"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 140},
		{"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 90},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 140},
		{"label": "Potential Misstatement", "fieldname": "potential_misstatement_amount", "fieldtype": "Currency", "width": 160},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "severity", "status", "fs_area"):
		if filters.get(field):
			conditions[field] = filters[field]

	return frappe.get_all(
		"Audit Finding",
		filters=conditions,
		fields=[
			"name", "engagement", "finding_title", "fs_area", "category", "severity", "status",
			"potential_misstatement_amount",
		],
		order_by="field(severity, 'Critical', 'High', 'Medium', 'Low')",
	)
