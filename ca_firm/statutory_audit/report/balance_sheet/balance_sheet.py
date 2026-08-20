import frappe

from ca_firm.utils.financial_statement import build_statement_rows, get_line_item_amounts

# Generated live off the engagement's Trial Balance via the FS Line Item
# hierarchy -- not a static template. Reflects Trial Balance mapped
# balances only; current-year profit is not auto-posted into Retained
# Earnings/Equity, since that's a closing entry a preparer should make
# deliberately once the P&L side is finalized, not something to infer.


def execute(filters=None):
	filters = filters or {}
	if not filters.get("engagement"):
		frappe.throw("Select an Engagement to generate the Balance Sheet for.")

	columns = get_columns()
	amounts = get_line_item_amounts(filters["engagement"])
	data = build_statement_rows("Balance Sheet", amounts)
	return columns, data


def get_columns():
	return [
		{"label": "Line Item", "fieldname": "line_item", "fieldtype": "Data", "width": 320},
		{"label": "Current Year", "fieldname": "current_year", "fieldtype": "Currency", "width": 150},
		{"label": "Prior Year", "fieldname": "prior_year", "fieldtype": "Currency", "width": 150},
	]
