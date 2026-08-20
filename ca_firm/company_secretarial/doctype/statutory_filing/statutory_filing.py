import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class StatutoryFiling(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""A statutory filing that affects a Trial Balance head (e.g. a
		charge registration affecting Liabilities, an allotment affecting
		Share Capital) is worth the statutory auditor knowing about for
		the same client and financial year."""
		if not self.linked_head:
			frappe.throw("Set a Linked Head before escalating this filing.")

		client, financial_year = frappe.db.get_value(
			"Company Secretarial Engagement", self.engagement, ["client", "financial_year"]
		)
		if not client:
			frappe.throw("This filing's engagement has no client set.")

		audit_engagement = frappe.db.get_value(
			"Statutory Audit Engagement",
			{"client": client, "financial_year": financial_year},
			"name",
		)
		if not audit_engagement:
			frappe.throw(
				"No Statutory Audit Engagement found for this client and financial year to escalate to."
			)

		create_cross_reference(
			source_doctype="Statutory Filing",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="Shares Financial Head",
			client=client,
			linked_head=self.linked_head,
			remarks=f"Statutory Filing {self.name} ({self.filing_type}) escalated for audit consideration.",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
