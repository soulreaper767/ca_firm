import frappe
from frappe.model.document import Document

from ca_firm.utils.financial_statement import get_line_item_amounts


class CashFlowStatement(Document):
	def validate(self):
		self.net_cash_from_operating = sum(frappe.utils.flt(r.amount) for r in self.operating_activities)
		self.net_cash_from_investing = sum(frappe.utils.flt(r.amount) for r in self.investing_activities)
		self.net_cash_from_financing = sum(frappe.utils.flt(r.amount) for r in self.financing_activities)
		self.net_increase_decrease_in_cash = (
			self.net_cash_from_operating + self.net_cash_from_investing + self.net_cash_from_financing
		)
		self.closing_cash_balance = (
			frappe.utils.flt(self.opening_cash_balance) + self.net_increase_decrease_in_cash
		)

	def _bs_lines_by_classification(self, classifications):
		amounts = get_line_item_amounts(self.engagement)
		lines = frappe.get_all(
			"FS Line Item",
			filters={"statement_type": "Balance Sheet", "classification": ["in", classifications], "is_subtotal": 0},
			fields=["name", "line_item_name"],
		)
		return [(l.line_item_name, amounts.get(l.name, (0.0, 0.0))) for l in lines]

	@frappe.whitelist()
	def pull_draft_operating_activities(self):
		"""Starting draft only: net profit for the year, plus the
		year-on-year change in each Current Asset/Liability line (an
		increase in a current asset is a cash outflow, an increase in a
		current liability is a cash inflow). Does not add back non-cash
		items (depreciation, provisions) or exclude cash/cash-equivalent
		lines from working capital -- review and adjust both before relying
		on this."""
		if not self.engagement:
			frappe.throw("Link an Engagement first.")

		pl_lines = frappe.get_all(
			"FS Line Item",
			filters={"statement_type": "Profit and Loss", "classification": ["in", ["Income", "Expense"]]},
			fields=["name", "classification"],
		)
		amounts = get_line_item_amounts(self.engagement)
		net_profit = sum(
			(amounts.get(l.name, (0.0, 0.0))[0] if l.classification == "Income" else -amounts.get(l.name, (0.0, 0.0))[0])
			for l in pl_lines
		)

		self.set("operating_activities", [])
		self.append("operating_activities", {"description": "Net Profit for the Year", "amount": net_profit})
		for label, (cur, prior) in self._bs_lines_by_classification(["Asset - Current"]):
			self.append("operating_activities", {
				"description": f"(Increase)/Decrease in {label}", "amount": -(cur - prior),
			})
		for label, (cur, prior) in self._bs_lines_by_classification(["Liability - Current"]):
			self.append("operating_activities", {
				"description": f"Increase/(Decrease) in {label}", "amount": cur - prior,
			})
		self.save()

	@frappe.whitelist()
	def pull_draft_investing_activities(self):
		"""Starting draft: the year-on-year change in each Non-Current Asset
		line, treated as a straight capex/disposal proxy -- this conflates
		additions, disposals, and depreciation into one net movement, so
		break it out manually where any of those happened during the year."""
		if not self.engagement:
			frappe.throw("Link an Engagement first.")

		self.set("investing_activities", [])
		for label, (cur, prior) in self._bs_lines_by_classification(["Asset - Non Current"]):
			self.append("investing_activities", {
				"description": f"(Increase)/Decrease in {label}", "amount": -(cur - prior),
			})
		self.save()

	@frappe.whitelist()
	def pull_draft_financing_activities(self):
		"""Starting draft: the year-on-year change in each Non-Current
		Liability and Equity line. Dividends paid, share issues, and loan
		drawdowns/repayments should be reviewed individually rather than
		relied on as one net movement per line."""
		if not self.engagement:
			frappe.throw("Link an Engagement first.")

		self.set("financing_activities", [])
		for label, (cur, prior) in self._bs_lines_by_classification(["Liability - Non Current", "Equity"]):
			self.append("financing_activities", {
				"description": f"Increase/(Decrease) in {label}", "amount": cur - prior,
			})
		self.save()
