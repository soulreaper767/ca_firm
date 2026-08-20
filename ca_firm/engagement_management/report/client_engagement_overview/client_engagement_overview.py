import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Client Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Services", "fieldname": "services_summary", "fieldtype": "Data", "width": 260},
		{"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Agreement Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
		{"label": "Total Fee", "fieldname": "total_fee_amount", "fieldtype": "Currency", "width": 120},
	]


def get_data(filters):
	conditions = {}
	if filters.get("client"):
		conditions["client"] = filters["client"]
	if filters.get("status"):
		conditions["status"] = filters["status"]
	if filters.get("engagement_partner"):
		conditions["engagement_partner"] = filters["engagement_partner"]

	records = frappe.get_all(
		"Client Engagement",
		filters=conditions,
		fields=["name", "client", "engagement_partner", "status", "total_fee_amount"],
		order_by="modified desc",
	)
	if not records:
		return records

	names = [r.name for r in records]
	service_rows = frappe.get_all(
		"Client Engagement Service",
		filters={"parent": ["in", names]},
		fields=["parent", "engagement_type", "stage"],
	)
	by_parent = {}
	for row in service_rows:
		by_parent.setdefault(row.parent, []).append(f"{row.engagement_type} ({row.stage})")

	for r in records:
		r["services_summary"] = ", ".join(by_parent.get(r.name, []))
	return records
