import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Data", "width": 110},
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Engagement", "width": 140},
		{"label": "Engagement Type", "fieldname": "engagement_type", "fieldtype": "Data", "width": 130},
		{"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Staff Member", "width": 130},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Opinion", "fieldname": "opinion_type", "fieldtype": "Data", "width": 110},
	]


def get_data(filters):
	conditions = {}
	if filters.get("client"):
		conditions["client"] = filters["client"]

	engagements = frappe.get_all(
		"Engagement",
		filters=conditions,
		fields=["name", "client", "financial_year", "engagement_type", "engagement_partner", "status"],
		order_by="client asc, financial_year desc",
	)
	opinions = {
		r.engagement: r.opinion_type
		for r in frappe.get_all("Audit Report", fields=["engagement", "opinion_type"])
	}
	for row in engagements:
		row["opinion_type"] = opinions.get(row.name)
	return engagements
