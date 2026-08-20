import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Filing", "fieldname": "name", "fieldtype": "Link", "options": "Statutory Filing", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Company Secretarial Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Filing Type", "fieldname": "filing_type", "fieldtype": "Link", "options": "Statutory Filing Type", "width": 170},
		{"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": "Filing Date", "fieldname": "filing_date", "fieldtype": "Date", "width": 100},
		{"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "status"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Statutory Filing", filters=conditions,
		fields=["name", "engagement", "filing_type", "due_date", "filing_date", "status"],
		order_by="due_date asc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Company Secretarial Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}

	today = frappe.utils.getdate()
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
		if r.due_date and r.status != "Filed" and not r.filing_date:
			overdue = (today - r.due_date).days
			r["days_overdue"] = overdue if overdue > 0 else 0
		else:
			r["days_overdue"] = 0
	return records
