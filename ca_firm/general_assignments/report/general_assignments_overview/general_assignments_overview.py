import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Assignment", "fieldname": "name", "fieldtype": "Link", "options": "General Assignment", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Description", "fieldname": "assignment_description", "fieldtype": "Data", "width": 220},
		{"label": "Engagement Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Target Completion", "fieldname": "target_completion_date", "fieldtype": "Date", "width": 120},
		{"label": "Tasks Done", "fieldname": "tasks_done", "fieldtype": "Data", "width": 100},
		{"label": "% Complete", "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	conditions = {}
	for field in ("client", "status", "engagement_partner"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"General Assignment", filters=conditions,
		fields=["name", "client", "assignment_description", "engagement_partner",
		        "target_completion_date", "status"],
		order_by="target_completion_date asc",
	)
	if not records:
		return records

	names = [r.name for r in records]
	tasks = frappe.get_all(
		"Assignment Task", filters={"parent": ["in", names]}, fields=["parent", "status"],
	)
	total_by_parent = {}
	done_by_parent = {}
	for t in tasks:
		total_by_parent[t.parent] = total_by_parent.get(t.parent, 0) + 1
		if t.status == "Completed":
			done_by_parent[t.parent] = done_by_parent.get(t.parent, 0) + 1

	for r in records:
		total = total_by_parent.get(r.name, 0)
		done = done_by_parent.get(r.name, 0)
		r["tasks_done"] = f"{done}/{total}" if total else "0/0"
		r["percent_complete"] = round((done / total) * 100, 1) if total else 0
	return records
