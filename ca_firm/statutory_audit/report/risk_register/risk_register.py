import frappe


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "FS Area", "fieldname": "fs_area", "fieldtype": "Link", "options": "Financial Statement Area", "width": 160},
		{"label": "Assertion", "fieldname": "assertion", "fieldtype": "Link", "options": "Assertion", "width": 150},
		{"label": "Risk Description", "fieldname": "risk_description", "fieldtype": "Data", "width": 220},
		{"label": "Inherent Risk", "fieldname": "inherent_risk", "fieldtype": "Data", "width": 100},
		{"label": "Control Risk", "fieldname": "control_risk", "fieldtype": "Data", "width": 100},
		{"label": "RMM", "fieldname": "risk_of_material_misstatement", "fieldtype": "Data", "width": 100},
		{"label": "Planned Response", "fieldname": "planned_response", "fieldtype": "Data", "width": 220},
	]
	conditions = {}
	for field in ("engagement", "fs_area"):
		if filters.get(field):
			conditions[field] = filters[field]
	if filters.get("high_risk_only"):
		conditions["risk_of_material_misstatement"] = ["in", ["High", "Critical"]]
	data = frappe.get_all(
		"Risk Assessment", filters=conditions,
		fields=["engagement", "fs_area", "assertion", "risk_description", "inherent_risk",
		        "control_risk", "risk_of_material_misstatement", "planned_response"],
		order_by="modified desc",
	)
	return columns, data
