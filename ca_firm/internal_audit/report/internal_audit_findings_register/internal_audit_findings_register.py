import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Observation", "fieldname": "name", "fieldtype": "Link", "options": "Internal Audit Observation", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Internal Audit Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Area Reviewed", "fieldname": "area_reviewed", "fieldtype": "Data", "width": 150},
		{"label": "Risk Rating", "fieldname": "risk_rating", "fieldtype": "Link", "options": "Rating Scale", "width": 100},
		{"label": "Responsible Person", "fieldname": "responsible_person", "fieldtype": "Data", "width": 140},
		{"label": "Target Date", "fieldname": "target_date", "fieldtype": "Date", "width": 100},
		{"label": "Days Overdue", "fieldname": "days_overdue", "fieldtype": "Int", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "status", "risk_rating"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Internal Audit Observation", filters=conditions,
		fields=["name", "engagement", "area_reviewed", "risk_rating", "responsible_person",
		        "target_date", "status"],
		order_by="target_date asc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Internal Audit Engagement",
		filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}

	today = frappe.utils.getdate()
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
		if r.target_date and r.status != "Closed":
			overdue = (today - r.target_date).days
			r["days_overdue"] = overdue if overdue > 0 else 0
		else:
			r["days_overdue"] = 0
	return records
