import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Benchmark", "fieldname": "benchmark", "fieldtype": "Data", "width": 140},
		{"label": "Benchmark Amount", "fieldname": "benchmark_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Materiality %", "fieldname": "materiality_percent", "fieldtype": "Percent", "width": 100},
		{"label": "Overall Materiality", "fieldname": "overall_materiality", "fieldtype": "Currency", "width": 150},
		{"label": "Performance Materiality", "fieldname": "performance_materiality", "fieldtype": "Currency", "width": 170},
		{"label": "Clearly Trivial Threshold", "fieldname": "clearly_trivial_threshold", "fieldtype": "Currency", "width": 170},
		{"label": "Docstatus", "fieldname": "docstatus", "fieldtype": "Int", "width": 80},
	]


def get_data(filters):
	conditions = {}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]

	return frappe.get_all(
		"Materiality Workings",
		filters=conditions,
		fields=[
			"engagement", "benchmark", "benchmark_amount", "materiality_percent", "overall_materiality",
			"performance_materiality", "clearly_trivial_threshold", "docstatus",
		],
		order_by="modified desc",
	)
