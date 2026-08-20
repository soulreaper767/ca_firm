import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Task", "fieldname": "name", "fieldtype": "Link", "options": "Bookkeeping Task", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Bookkeeping Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Task Type", "fieldname": "task_type", "fieldtype": "Link", "options": "Bookkeeping Task Type", "width": 160},
		{"label": "Period", "fieldname": "period", "fieldtype": "Data", "width": 110},
		{"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": "Completion Date", "fieldname": "completion_date", "fieldtype": "Date", "width": 120},
		{"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "status", "task_type"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Bookkeeping Task", filters=conditions,
		fields=["name", "engagement", "task_type", "period", "due_date", "completion_date", "status"],
		order_by="due_date asc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Bookkeeping Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}

	today = frappe.utils.getdate()
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
		if r.due_date and not r.completion_date:
			overdue = (today - r.due_date).days
			r["days_overdue"] = overdue if overdue > 0 else 0
		else:
			r["days_overdue"] = 0
	return records
