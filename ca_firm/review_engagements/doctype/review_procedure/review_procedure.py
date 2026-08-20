import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class ReviewProcedure(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""A matter noted during a review often matters to the statutory
		auditor for the same client and period -- most commonly where a
		quarterly/interim review precedes the annual audit. Finds the
		Statutory Audit Engagement for the same client and financial year
		and raises a cross-reference against it."""
		if self.conclusion != "Matter Noted":
			frappe.throw("Only procedures concluding 'Matter Noted' need escalation.")

		client, financial_year = frappe.db.get_value(
			"Review Engagement", self.engagement, ["client", "financial_year"]
		)
		if not client:
			frappe.throw("This procedure's engagement has no client set.")

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
			source_doctype="Review Procedure",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="References Audit Finding",
			client=client,
			linked_head=self.linked_head,
			remarks=f"Review Procedure {self.name} ({self.area}) escalated: {self.analytical_result or ''}",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
