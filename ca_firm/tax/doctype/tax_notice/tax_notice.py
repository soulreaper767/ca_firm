import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class TaxNotice(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""A material tax notice (e.g. an assessment order raising a
		liability, or a notice referencing figures under audit) often
		matters to the statutory auditor too -- most commonly as a
		contingent liability / provision consideration. Finds the
		Statutory Audit Engagement for the same client and financial year
		and raises a two-way cross-reference against it, instead of the
		tax and audit teams tracking the same notice separately."""
		client = frappe.db.get_value("Tax Engagement", self.engagement, "client")
		if not client:
			frappe.throw("This Tax Notice's engagement has no client set.")

		audit_engagement = frappe.db.get_value(
			"Statutory Audit Engagement",
			{"client": client, "financial_year": self.tax_year},
			"name",
		)
		if not audit_engagement:
			frappe.throw(
				"No Statutory Audit Engagement found for this client and tax year to escalate to."
			)

		create_cross_reference(
			source_doctype="Tax Notice",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="Escalation",
			client=client,
			remarks=f"Tax Notice {self.name} ({self.notice_type}) escalated for audit consideration "
			f"(contingent liability / provision).",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
