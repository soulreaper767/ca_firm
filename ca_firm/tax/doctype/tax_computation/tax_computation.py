import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class TaxComputation(Document):
	def validate(self):
		self.tax_payable_or_refundable = (
			frappe.utils.flt(self.tax_liability)
			- frappe.utils.flt(self.advance_tax_paid)
			- frappe.utils.flt(self.withholding_tax_credit)
		)

	@frappe.whitelist()
	def pull_accounting_profit_from_audit(self):
		"""Where the same client also has a statutory audit for the same
		period, compute the accounting profit (before tax) from its Lead
		Schedule instead of the figure being re-keyed by hand: sum every
		Profit and Loss head classified Income, less every head classified
		Expense, excluding the Taxation line itself (that's the tax
		expense, not part of profit *before* tax)."""
		if not self.source_statutory_engagement:
			frappe.throw("Link a Statutory Audit Engagement first.")

		tb_name = frappe.db.get_value(
			"Trial Balance", {"engagement": self.source_statutory_engagement}, "name"
		)
		if not tb_name:
			frappe.throw("The linked engagement has no Trial Balance on file yet.")

		pnl_lines = frappe.get_all(
			"FS Line Item",
			filters={
				"statement_type": "Profit and Loss",
				"classification": ["in", ["Income", "Expense"]],
				"line_item_name": ["!=", "Taxation"],
			},
			fields=["name", "classification"],
		)
		line_classification = {l.name: l.classification for l in pnl_lines}
		if not line_classification:
			frappe.throw("No Profit and Loss FS Line Items found to aggregate from.")

		heads = frappe.get_all(
			"Chart of Accounts Head", filters={"fs_line_item": ["in", list(line_classification.keys())]},
			fields=["name", "fs_line_item", "nature"],
		)
		if not heads:
			frappe.throw("No Chart of Accounts Head is mapped to any Profit and Loss line item.")
		head_info = {h.name: h for h in heads}

		entries = frappe.get_all(
			"Trial Balance Entry", filters={"parent": tb_name, "mapped_head": ["in", list(head_info.keys())]},
			fields=["mapped_head", "current_year_debit", "current_year_credit"],
		)

		profit = 0.0
		for e in entries:
			head = head_info.get(e.mapped_head)
			if not head:
				continue
			# Natural-balance amount: positive whenever the head sits on its
			# own normal side (a Debit-nature expense with debit > credit,
			# or a Credit-nature income with credit > debit both come out
			# positive here) -- same convention the Lead Schedule report uses.
			nature_sign = 1 if head.nature == "Debit" else -1
			natural_amount = nature_sign * (frappe.utils.flt(e.current_year_debit) - frappe.utils.flt(e.current_year_credit))
			classification = line_classification.get(head.fs_line_item)
			profit += natural_amount if classification == "Income" else -natural_amount

		self.accounting_profit = profit
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
