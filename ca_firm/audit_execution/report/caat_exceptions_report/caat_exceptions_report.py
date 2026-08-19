import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "CAAT Run", "fieldname": "parent", "fieldtype": "Link", "options": "CAAT Run", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Test Template", "fieldname": "test_template", "fieldtype": "Link", "options": "CAAT Test Template", "width": 220},
		{"label": "Record Reference", "fieldname": "record_reference", "fieldtype": "Data", "width": 140},
		{"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
		{"label": "Risk Level", "fieldname": "risk_level", "fieldtype": "Data", "width": 90},
		{"label": "Disposition", "fieldname": "disposition", "fieldtype": "Data", "width": 190},
	]


def get_data(filters):
	conditions = {}
	if filters.get("disposition"):
		conditions["disposition"] = filters["disposition"]
	else:
		conditions["disposition"] = "Pending"
	if filters.get("risk_level"):
		conditions["risk_level"] = filters["risk_level"]

	exceptions = frappe.get_all(
		"CAAT Exception",
		filters=conditions,
		fields=["parent", "record_reference", "description", "amount", "risk_level", "disposition"],
	)
	if not exceptions:
		return exceptions

	run_names = list({e.parent for e in exceptions})
	runs = {
		r.name: r
		for r in frappe.get_all(
			"CAAT Run", filters={"name": ["in", run_names]}, fields=["name", "engagement", "test_template"]
		)
	}
	for row in exceptions:
		run = runs.get(row.parent)
		if run:
			row["engagement"] = run.engagement
			row["test_template"] = run.test_template
	return exceptions
