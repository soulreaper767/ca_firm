import frappe
from frappe.model.document import Document

from ca_firm.utils.financial_statement import get_line_item_amounts


class StatementofChangesinEquity(Document):
	def validate(self):
		for row in self.components:
			row.closing_balance = (
				frappe.utils.flt(row.opening_balance)
				+ frappe.utils.flt(row.profit_for_the_year)
				+ frappe.utils.flt(row.other_comprehensive_income)
				+ frappe.utils.flt(row.dividends_declared)
				+ frappe.utils.flt(row.share_capital_issued)
				+ frappe.utils.flt(row.other_movements)
			)
		self.total_closing_equity = sum(frappe.utils.flt(r.closing_balance) for r in self.components)

	@frappe.whitelist()
	def pull_opening_closing_balances(self):
		"""Starting draft only: opening and closing balances per
		Equity-classified Balance Sheet line, taken straight from the prior
		and current year Trial Balance. The movement columns in between
		(profit for the year, OCI, dividends, share issues) aren't
		derivable from a Trial Balance alone -- fill them in based on what
		actually happened during the year, then Closing Balance should tie
		back to what's pulled here."""
		if not self.engagement:
			frappe.throw("Link an Engagement first.")

		amounts = get_line_item_amounts(self.engagement)
		lines = frappe.get_all(
			"FS Line Item",
			filters={"statement_type": "Balance Sheet", "classification": "Equity", "is_subtotal": 0},
			fields=["name", "line_item_name"],
		)
		if not lines:
			frappe.throw("No Equity-classified FS Line Items found.")

		self.set("components", [])
		for l in lines:
			cur, prior = amounts.get(l.name, (0.0, 0.0))
			self.append("components", {
				"equity_component": l.line_item_name,
				"opening_balance": prior,
				"tb_closing_balance": cur,
			})
		self.save()
