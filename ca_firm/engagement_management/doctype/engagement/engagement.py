import frappe
from frappe.model.document import Document


class Engagement(Document):
	def validate(self):
		self.set_engagement_name()
		self.validate_eqcr()

	def set_engagement_name(self):
		client_name = frappe.db.get_value("Client", self.client, "client_name") if self.client else None
		parts = [client_name or self.client, self.financial_year, self.engagement_type]
		self.engagement_name = " - ".join([p for p in parts if p])

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
