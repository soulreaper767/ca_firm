import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference
from ca_firm.utils.financial_statement import get_line_item_amounts


class TaxComputation(Document):
	def validate(self):
		self.tax_payable_or_refundable = (
			frappe.utils.flt(self.tax_liability)
			- frappe.utils.flt(self.advance_tax_paid)
			- frappe.utils.flt(self.withholding_tax_credit)
		)

	def _pl_amounts_excluding_taxation(self):
		"""(fs_line_item -> (classification, current_year_amount)) for every
		Profit and Loss line except Taxation itself -- shared by both the
		single-figure pull and the full-breakdown pull so they can never
		disagree with each other."""
		if not self.source_statutory_engagement:
			frappe.throw("Link a Source Statutory Engagement first.")

		amounts = get_line_item_amounts(self.source_statutory_engagement)
		if not amounts:
			frappe.throw("The linked engagement has no Trial Balance on file yet.")

		pnl_lines = frappe.get_all(
			"FS Line Item",
			filters={
				"statement_type": "Profit and Loss",
				"classification": ["in", ["Income", "Expense"]],
				"line_item_name": ["!=", "Taxation"],
			},
			fields=["name", "line_item_name", "classification"],
		)
		if not pnl_lines:
			frappe.throw("No Profit and Loss FS Line Items found to aggregate from.")

		return {l.name: (l.classification, amounts.get(l.name, (0.0, 0.0))[0]) for l in pnl_lines}

	@frappe.whitelist()
	def pull_accounting_profit_from_audit(self):
		"""Where the same client also has a statutory audit for the same
		period, compute the accounting profit (before tax) from its Trial
		Balance instead of the figure being re-keyed by hand: sum every
		Profit and Loss line classified Income, less every line classified
		Expense, excluding the Taxation line itself (that's the tax
		expense, not part of profit *before* tax)."""
		lines = self._pl_amounts_excluding_taxation()
		profit = sum(
			amount if classification == "Income" else -amount
			for classification, amount in lines.values()
		)
		self.accounting_profit = profit
		self.save()

	@frappe.whitelist()
	def pull_full_pl_breakdown(self):
		"""Not just the single accounting-profit total: every Profit and
		Loss FS Line Item's amount from the linked audit, so the preparer
		can see and adjust each element -- revenue, cost of sales, each
		expense head -- individually. Replaces any existing P&L Lines."""
		lines = self._pl_amounts_excluding_taxation()
		self.set("pl_lines", [])
		for fs_line, (classification, amount) in lines.items():
			self.append("pl_lines", {
				"fs_line_item": fs_line, "classification": classification, "amount": amount,
			})
		self.save()

	@frappe.whitelist()
	def compute_from_adjustment_items(self):
		"""Total the structured Adjustment Items table straight into Taxable
		Income, instead of the preparer re-adding the Add Back / Allowance
		narrative fields by hand: Taxable Income = Accounting Profit + all
		Add Back amounts - all Allowance amounts."""
		add_backs = sum(
			frappe.utils.flt(i.amount) for i in self.adjustment_items if i.adjustment_type == "Add Back"
		)
		allowances = sum(
			frappe.utils.flt(i.amount) for i in self.adjustment_items if i.adjustment_type == "Allowance"
		)
		self.taxable_income = frappe.utils.flt(self.accounting_profit) + add_backs - allowances
		self.save()

	@frappe.whitelist()
	def flag_items_to_audit(self):
		"""Any Adjustment Item ticked 'Also Needs Audit Adjustment' is raised
		as a cross-reference against the linked Statutory Audit Engagement,
		tagged with the specific head it affects -- so the audit team can
		see, from their own working papers, which of the tax team's
		adjustments also has audit-side impact (e.g. a disallowed
		provision that also needs a corresponding Audit Adjustment)."""
		if not self.source_statutory_engagement:
			frappe.throw("Link a Source Statutory Engagement first.")

		flagged = [i for i in self.adjustment_items if i.flag_to_audit]
		if not flagged:
			frappe.msgprint("No adjustment items are flagged for audit attention.")
			return

		client = frappe.db.get_value(
			"Statutory Audit Engagement", self.source_statutory_engagement, "client"
		)
		for item in flagged:
			create_cross_reference(
				source_doctype="Tax Computation",
				source_name=self.name,
				target_doctype="Statutory Audit Engagement",
				target_name=self.source_statutory_engagement,
				relationship_type="Raises Audit Adjustment",
				client=client,
				linked_head=item.head,
				remarks=f"{item.adjustment_type}: {item.description} ({frappe.utils.fmt_money(item.amount)})",
			)
		frappe.msgprint(f"Raised {len(flagged)} cross-reference(s) against {self.source_statutory_engagement}.")
