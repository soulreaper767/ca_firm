import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Count Sheet", "fieldname": "name", "fieldtype": "Link", "options": "Inventory Count Sheet", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Inventory Audit Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Location", "fieldname": "location", "fieldtype": "Data", "width": 130},
		{"label": "Count Date", "fieldname": "count_date", "fieldtype": "Date", "width": 100},
		{"label": "Items Counted", "fieldname": "item_count", "fieldtype": "Int", "width": 100},
		{"label": "Items With Variance", "fieldname": "variance_count", "fieldtype": "Int", "width": 130},
		{"label": "Total Variance Value", "fieldname": "total_variance_value", "fieldtype": "Currency", "width": 140},
	]


def get_data(filters):
	conditions = {}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]

	records = frappe.get_all(
		"Inventory Count Sheet", filters=conditions,
		fields=["name", "engagement", "location", "count_date", "total_variance_value"],
		order_by="count_date desc",
	)
	if not records:
		return records

	names = [r.name for r in records]
	items = frappe.get_all(
		"Inventory Count Item", filters={"parent": ["in", names]},
		fields=["parent", "book_quantity", "counted_quantity"],
	)
	item_count = {}
	variance_count = {}
	for i in items:
		item_count[i.parent] = item_count.get(i.parent, 0) + 1
		if frappe.utils.flt(i.book_quantity) != frappe.utils.flt(i.counted_quantity):
			variance_count[i.parent] = variance_count.get(i.parent, 0) + 1

	engagements = frappe.get_all(
		"Inventory Audit Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}

	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
		r["item_count"] = item_count.get(r.name, 0)
		r["variance_count"] = variance_count.get(r.name, 0)
	return records
