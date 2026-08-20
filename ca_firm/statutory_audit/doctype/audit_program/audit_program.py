import frappe
from frappe.model.document import Document


class AuditProgram(Document):
	def validate(self):
		if self.template_used and not self.steps:
			self.populate_from_template()

	@frappe.whitelist()
	def populate_from_template(self):
		if not self.template_used:
			return
		profile = self._engagement_profile()
		template = frappe.get_doc("Audit Program Template", self.template_used)
		self.steps = []
		for row in template.steps:
			if row.applicable_entity_size and row.applicable_entity_size != profile.get("entity_size_category"):
				continue
			self.append("steps", {
				"step_no": row.step_no,
				"procedure_description": row.procedure_description,
				"assertion": row.assertion,
				"procedure_type": row.procedure_type,
				"is_caat": row.is_caat,
			})

	def _engagement_profile(self):
		if not self.engagement:
			return {}
		return frappe.db.get_value(
			"Statutory Audit Engagement", self.engagement, ["entity_size_category"], as_dict=True
		) or {}
