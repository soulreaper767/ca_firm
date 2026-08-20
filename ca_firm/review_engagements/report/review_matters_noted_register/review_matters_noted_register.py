import frappe

# Every Review Procedure that came back "Matter Noted" instead of "Nothing
# Has Come to Our Attention" -- the review-engagement equivalent of an audit
# findings register, since ISRE 2400 reviews conclude on exceptions found
# through inquiry and analytical procedures rather than a full opinion.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Procedure", "fieldname": "name", "fieldtype": "Link", "options": "Review Procedure", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Review Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Area", "fieldname": "area", "fieldtype": "Data", "width": 150},
		{"label": "Analytical Result", "fieldname": "analytical_result", "fieldtype": "Data", "width": 200},
		{"label": "Performed By", "fieldname": "performed_by", "fieldtype": "Link", "options": "Employee", "width": 130},
	]


def get_data(filters):
	conditions = {"conclusion": "Matter Noted"}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]

	records = frappe.get_all(
		"Review Procedure", filters=conditions,
		fields=["name", "engagement", "area", "analytical_result", "performed_by"],
		order_by="modified desc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Review Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
	return records
