import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class AdvisoryRecommendation(Document):
	@frappe.whitelist()
	def escalate_to_audit(self):
		"""An implemented advisory recommendation that affects a specific
		head (e.g. a revised valuation methodology, a provisioning policy
		change) is worth the statutory auditor knowing about for the same
		client and financial year, since it may change what they expect
		to see in that head."""
		if not self.linked_head:
			frappe.throw("Set a Linked Head before escalating this recommendation.")

		client, financial_year = frappe.db.get_value(
			"Advisory Engagement", self.engagement, ["client", "financial_year"]
		)
		if not client:
			frappe.throw("This recommendation's engagement has no client set.")

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
			source_doctype="Advisory Recommendation",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="Shares Financial Head",
			client=client,
			linked_head=self.linked_head,
			remarks=f"Advisory Recommendation {self.name} ({self.recommendation_area or ''}) "
			f"escalated for audit consideration.",
		)
		frappe.msgprint(f"Escalated to Statutory Audit Engagement {audit_engagement}.")
