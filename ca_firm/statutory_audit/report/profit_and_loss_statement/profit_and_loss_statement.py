import frappe

from ca_firm.utils.financial_statement import build_statement_rows, get_line_item_amounts


def execute(filters=None):
	filters = filters or {}
	if not filters.get("engagement"):
		frappe.throw("Select an Engagement to generate the Profit and Loss Statement for.")

	columns = get_columns()
	amounts = get_line_item_amounts(filters["engagement"])
	data = build_statement_rows("Profit and Loss", amounts)
	return columns, data


def get_columns():
	return [
		{"label": "Line Item", "fieldname": "line_item", "fieldtype": "Data", "width": 320},
		{"label": "Current Year", "fieldname": "current_year", "fieldtype": "Currency", "width": 150},
		{"label": "Prior Year", "fieldname": "prior_year", "fieldtype": "Currency", "width": 150},
	]
