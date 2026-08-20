import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class GeneralAssignment(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""Even a generic assignment can occasionally surface something the
		statutory auditor for the same client and financial year should
		know about. Finds the matching Statutory Audit Engagement and
		raises a cross-reference against it."""
		if not self.linked_head:
			frappe.throw("Set a Linked Head before escalating this assignment.")

		audit_engagement = frappe.db.get_value(
			"Statutory Audit Engagement",
			{"client": self.client, "financial_year": self.financial_year},
			"name",
		)
		if not audit_engagement:
			frappe.throw(
				"No Statutory Audit Engagement found for this client and financial year to escalate to."
			)

		create_cross_reference(
			source_doctype="General Assignment",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="Shares Financial Head",
			client=self.client,
			linked_head=self.linked_head,
			remarks=f"General Assignment {self.name} escalated for audit consideration.",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
