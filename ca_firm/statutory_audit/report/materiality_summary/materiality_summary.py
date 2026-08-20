import frappe


def execute(filters=None):
	filters = filters or {}
	columns = [
		{"label": "Working", "fieldname": "name", "fieldtype": "Link", "options": "Materiality Workings", "width": 120},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Benchmark", "fieldname": "benchmark", "fieldtype": "Data", "width": 130},
		{"label": "Benchmark Amount", "fieldname": "benchmark_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Materiality %", "fieldname": "materiality_percent", "fieldtype": "Percent", "width": 100},
		{"label": "Overall Materiality", "fieldname": "overall_materiality", "fieldtype": "Currency", "width": 140},
		{"label": "Performance Materiality", "fieldname": "performance_materiality", "fieldtype": "Currency", "width": 160},
	]
	conditions = {}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]
	rows = frappe.get_all(
		"Materiality Workings", filters=conditions,
		fields=["name", "engagement", "benchmark", "benchmark_amount", "materiality_percent",
		        "overall_materiality", "performance_materiality"],
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
	return columns, rows
