import frappe
from frappe.model.document import Document


class StatutoryAuditEngagement(Document):
	def validate(self):
		self.validate_eqcr()

	def validate_eqcr(self):
		if self.is_eqcr_required and not self.eqcr_partner:
			frappe.msgprint(
				"EQCR is marked as required for this engagement but no EQCR Partner has been assigned.",
				indicator="orange",
				alert=True,
			)

	def on_update(self):
		if self.status == "Completed" and not self.actual_completion_date:
			self.db_set("actual_completion_date", frappe.utils.today())
