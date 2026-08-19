import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Record", "fieldname": "name", "fieldtype": "Dynamic Link", "options": "record_type", "width": 130},
		{"label": "Type", "fieldname": "record_type", "fieldtype": "Data", "width": 130},
		{"label": "Description", "fieldname": "description", "fieldtype": "Data", "width": 220},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 130},
		{"label": "Responsible", "fieldname": "responsible", "fieldtype": "Link", "options": "Employee", "width": 150},
	]


def get_data(filters):
	conditions = {}
	if filters.get("client"):
		conditions["client"] = filters["client"]

	rows = []
	for eng in frappe.get_all(
		"Engagement",
		filters=conditions,
		fields=["name", "client", "engagement_type", "financial_year", "status", "engagement_partner"],
	):
		rows.append({
			"client": eng.client,
			"name": eng.name,
			"record_type": "Engagement",
			"description": f"{eng.engagement_type or ''} - {eng.financial_year or ''}",
			"status": eng.status,
			"responsible": eng.engagement_partner,
		})

	for fee in frappe.get_all(
		"Client Fee Arrangement",
		filters=conditions,
		fields=["name", "client", "engagement_type", "fee_amount", "billing_frequency", "status", "agreed_by"],
	):
		rows.append({
			"client": fee.client,
			"name": fee.name,
			"record_type": "Client Fee Arrangement",
			"description": f"{fee.engagement_type or 'General'} - {fee.billing_frequency or ''}",
			"status": fee.status,
			"responsible": fee.agreed_by,
		})

	rows.sort(key=lambda r: (r["client"] or "", r["record_type"]))
	return rows
