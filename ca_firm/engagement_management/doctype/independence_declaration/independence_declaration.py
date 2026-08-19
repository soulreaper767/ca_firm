import frappe
from frappe.model.document import Document


class IndependenceDeclaration(Document):
	def validate(self):
		self.validate_threats_vs_declaration()

	def validate_threats_vs_declaration(self):
		threat_fields = [
			"has_financial_interest", "has_family_employment_relationship",
			"has_prior_employment_with_client", "provided_non_audit_services",
			"self_interest_threat", "self_review_threat", "advocacy_threat",
			"familiarity_threat", "intimidation_threat",
		]
		any_threat = any(self.get(field) for field in threat_fields)
		if any_threat and self.overall_declaration == "Independent":
			frappe.throw(
				"One or more independence threats have been identified. Please select "
				"'Independent with Safeguards' (with safeguards documented) or 'Not Independent'."
			)
		if self.overall_declaration == "Independent with Safeguards" and not self.safeguards_applied:
			frappe.throw("Please document the safeguards applied for this declaration.")
