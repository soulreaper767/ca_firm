import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Tax Notice", "fieldname": "name", "fieldtype": "Link", "options": "Tax Notice", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Tax Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Notice Type", "fieldname": "notice_type", "fieldtype": "Link", "options": "Tax Notice Type", "width": 150},
		{"label": "Notice Date", "fieldname": "notice_date", "fieldtype": "Date", "width": 100},
		{"label": "Response Deadline", "fieldname": "response_deadline", "fieldtype": "Date", "width": 120},
		{"label": "Days To Deadline", "fieldname": "days_to_deadline", "fieldtype": "Int", "width": 110},
		{"label": "Amount Involved", "fieldname": "amount_involved", "fieldtype": "Currency", "width": 120},
		{"label": "Assigned To", "fieldname": "assigned_to", "fieldtype": "Link", "options": "Employee", "width": 130},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	conditions = {"status": ["not in", ["Resolved", "Closed"]]}
	for field in ("engagement", "status"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Tax Notice", filters=conditions,
		fields=["name", "engagement", "notice_type", "notice_date", "response_deadline",
		        "amount_involved", "assigned_to", "status"],
		order_by="response_deadline asc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Tax Engagement",
		filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}

	today = frappe.utils.getdate()
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
		r["days_to_deadline"] = (r.response_deadline - today).days if r.response_deadline else None
	return records
