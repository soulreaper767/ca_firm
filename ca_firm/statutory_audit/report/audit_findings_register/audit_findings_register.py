import frappe


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": "Finding", "fieldname": "name", "fieldtype": "Link", "options": "Audit Finding", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "FS Area", "fieldname": "fs_area", "fieldtype": "Link", "options": "Financial Statement Area", "width": 150},
		{"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 90},
		{"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 140},
		{"label": "Potential Misstatement", "fieldname": "potential_misstatement_amount", "fieldtype": "Currency", "width": 150},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
	]
	conditions = {}
	for field in ("engagement", "fs_area", "status", "severity"):
		if filters.get(field):
			conditions[field] = filters[field]
	data = frappe.get_all(
		"Audit Finding", filters=conditions,
		fields=["name", "engagement", "fs_area", "severity", "category",
		        "potential_misstatement_amount", "status"],
		order_by="modified desc",
	)
	return columns, data
