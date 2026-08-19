import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Declaration Date", "fieldname": "declaration_date", "fieldtype": "Date", "width": 110},
		{"label": "Overall Declaration", "fieldname": "overall_declaration", "fieldtype": "Data", "width": 160},
		{"label": "Flags Raised", "fieldname": "flags", "fieldtype": "Data", "width": 260},
	]


def get_data(filters):
	"""Firm-wide view: every threat/flag ever declared, across all clients and
	years, for the given staff member (or everyone, if unfiltered) -- so a
	new-client acceptance check can see the person's full conflict history,
	not just what's on file for a single engagement."""
	conditions = {}
	if filters.get("staff_member"):
		conditions["staff_member"] = filters["staff_member"]
	if filters.get("client"):
		conditions["client"] = filters["client"]
	if filters.get("flags_only"):
		conditions["overall_declaration"] = ["!=", "Independent"]

	threat_fields = [
		"has_financial_interest", "has_family_employment_relationship",
		"has_prior_employment_with_client", "provided_non_audit_services",
		"self_interest_threat", "self_review_threat", "advocacy_threat",
		"familiarity_threat", "intimidation_threat",
	]
	records = frappe.get_all(
		"Independence Declaration",
		filters=conditions,
		fields=["name", "staff_member", "engagement", "client", "declaration_date", "overall_declaration"]
		+ threat_fields,
		order_by="staff_member asc, declaration_date desc",
	)
	rows = []
	for r in records:
		flags = [f.replace("_", " ").title() for f in threat_fields if r.get(f)]
		r["flags"] = ", ".join(flags) if flags else ""
		rows.append(r)
	return rows
