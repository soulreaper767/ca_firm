import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Certificate", "fieldname": "name", "fieldtype": "Link", "options": "Certificate Issued", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Certification Engagement", "width": 130},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Certificate Type", "fieldname": "certificate_type", "fieldtype": "Link", "options": "Certificate Type", "width": 160},
		{"label": "Addressee", "fieldname": "addressee", "fieldtype": "Data", "width": 150},
		{"label": "Amount Certified", "fieldname": "amount_certified", "fieldtype": "Currency", "width": 130},
		{"label": "Issue Date", "fieldname": "issue_date", "fieldtype": "Date", "width": 100},
		{"label": "Valid Until", "fieldname": "valid_until", "fieldtype": "Date", "width": 100},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "status", "certificate_type"):
		if filters.get(field):
			conditions[field] = filters[field]

	records = frappe.get_all(
		"Certificate Issued", filters=conditions,
		fields=["name", "engagement", "certificate_type", "addressee", "amount_certified",
		        "issue_date", "valid_until", "status"],
		order_by="issue_date desc",
	)
	if not records:
		return records

	engagements = frappe.get_all(
		"Certification Engagement", filters={"name": ["in", [r.engagement for r in records]]},
		fields=["name", "client"],
	)
	client_by_engagement = {e.name: e.client for e in engagements}
	for r in records:
		r["client"] = client_by_engagement.get(r.engagement)
	return records
