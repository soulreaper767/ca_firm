import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class InternalAuditObservation(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""A material internal audit observation (a control deficiency, a
		misstatement found in testing) often matters to the statutory
		auditor covering the same period -- it can affect their risk
		assessment or point to a misstatement worth testing independently.
		Finds the Statutory Audit Engagement for the same client and
		financial year and raises a two-way cross-reference against it,
		tagged to the affected head if one was recorded."""
		client, financial_year = frappe.db.get_value(
			"Internal Audit Engagement", self.engagement, ["client", "financial_year"]
		)
		if not client:
			frappe.throw("This observation's engagement has no client set.")

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
			source_doctype="Internal Audit Observation",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="References Audit Finding",
			client=client,
			linked_head=self.linked_head,
			remarks=f"Internal Audit Observation {self.name} ({self.area_reviewed}, "
			f"risk: {self.risk_rating or 'unrated'}) escalated for audit consideration.",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
