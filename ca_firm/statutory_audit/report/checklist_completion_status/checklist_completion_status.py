import frappe


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": "Checklist", "fieldname": "name", "fieldtype": "Link", "options": "Checklist Instance", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Template", "fieldname": "template", "fieldtype": "Link", "options": "Checklist Template", "width": 220},
		{"label": "Applicable Items", "fieldname": "applicable_items", "fieldtype": "Int", "width": 110},
		{"label": "Completed", "fieldname": "completed_items", "fieldtype": "Int", "width": 90},
		{"label": "% Complete", "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
	]
	conditions = {}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]
	rows = frappe.get_all(
		"Checklist Instance", filters=conditions,
		fields=["name", "engagement", "template", "applicable_items", "completed_items"],
		order_by="modified desc",
	)
	if not rows:
		return columns, rows
	eng_names = list({r.engagement for r in rows if r.engagement})
	client_map = {
		e.name: e.client
		for e in frappe.get_all("Statutory Audit Engagement", filters={"name": ["in", eng_names]}, fields=["name", "client"])
	}
	for r in rows:
		r["client"] = client_map.get(r.engagement)
		r["percent_complete"] = (r.completed_items / r.applicable_items * 100) if r.applicable_items else 0
	return columns, rows
