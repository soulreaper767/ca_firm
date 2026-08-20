import frappe

# Firm-wide view across all engagements, so a Partner reviewing a new client
# acceptance (or a periodic quality check) can see every declaration on file
# for a staff member -- not just what's recorded on one engagement -- and any
# conflict or non-independence flag stands out immediately.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "parent", "fieldtype": "Link", "options": "Client Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Declaration Date", "fieldname": "declaration_date", "fieldtype": "Date", "width": 110},
		{"label": "Declaration", "fieldname": "declaration", "fieldtype": "Data", "width": 170},
		{"label": "Has Conflict", "fieldname": "has_conflict", "fieldtype": "Check", "width": 100},
		{"label": "Conflict Details", "fieldname": "conflict_details", "fieldtype": "Data", "width": 220},
	]


def get_data(filters):
	conditions = {}
	if filters.get("staff_member"):
		conditions["staff_member"] = filters["staff_member"]
	if filters.get("flags_only"):
		conditions["declaration"] = ["!=", "Independent"]

	rows = frappe.get_all(
		"Client Engagement Independence Check",
		filters=conditions,
		fields=["parent", "staff_member", "declaration_date", "declaration", "has_conflict", "conflict_details"],
		order_by="staff_member asc, declaration_date desc",
	)
	if not rows:
		return rows

	parents = list({r.parent for r in rows})
	client_map = {
		e.name: e.client
		for e in frappe.get_all("Client Engagement", filters={"name": ["in", parents]}, fields=["name", "client"])
	}
	for r in rows:
		r["client"] = client_map.get(r.parent)
	return rows
