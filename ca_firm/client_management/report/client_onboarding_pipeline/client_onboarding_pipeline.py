import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Onboarding", "fieldname": "name", "fieldtype": "Link", "options": "Client Onboarding", "width": 130},
		{"label": "Client Name", "fieldname": "client_name", "fieldtype": "Data", "width": 200},
		{"label": "Entity Type", "fieldname": "entity_type", "fieldtype": "Link", "options": "Entity Type", "width": 150},
		{"label": "Assignment Types", "fieldname": "assignment_types", "fieldtype": "Data", "width": 220},
		{"label": "Engagement Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
		{"label": "Target Start", "fieldname": "target_start_date", "fieldtype": "Date", "width": 110},
		{"label": "Onboarded Client", "fieldname": "onboarded_client", "fieldtype": "Link", "options": "Customer", "width": 160},
	]


def get_data(filters):
	conditions = {}
	if filters.get("status"):
		conditions["status"] = filters["status"]
	if filters.get("engagement_partner"):
		conditions["engagement_partner"] = filters["engagement_partner"]

	records = frappe.get_all(
		"Client Onboarding",
		filters=conditions,
		fields=[
			"name", "client_name", "entity_type", "engagement_partner", "status",
			"target_start_date", "onboarded_client",
		],
		order_by="modified desc",
	)
	if not records:
		return records

	names = [r.name for r in records]
	assignment_rows = frappe.get_all(
		"Client Onboarding Assignment Type",
		filters={"parent": ["in", names]},
		fields=["parent", "engagement_type"],
	)
	by_parent = {}
	for row in assignment_rows:
		by_parent.setdefault(row.parent, []).append(row.engagement_type)

	for r in records:
		r["assignment_types"] = ", ".join(by_parent.get(r.name, []))
	return records
