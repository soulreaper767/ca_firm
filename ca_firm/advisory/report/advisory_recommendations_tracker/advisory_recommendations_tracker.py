import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Recommendation", "fieldname": "name", "fieldtype": "Link", "options": "Advisory Recommendation", "width": 140},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Advisory Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Area", "fieldname": "recommendation_area", "fieldtype": "Data", "width": 150},
		{"label": "Priority", "fieldname": "priority", "fieldtype": "Link", "options": "Priority Level", "width": 100},
		{"label": "Target Date", "fieldname": "target_date", "fieldtype": "Date", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "status", "priority"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Advisory Recommendation", filters=conditions,
		fields=["name", "engagement", "recommendation_area", "priority", "target_date", "status"],
		order_by="target_date asc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Advisory Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
	return records
