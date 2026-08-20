import frappe
from frappe.model.document import Document


class ClientEngagement(Document):
	def validate(self):
		self.set_engagement_name()
		self.total_fee_amount = sum(frappe.utils.flt(row.fee_amount) for row in self.services)

	def set_engagement_name(self):
		client_name = frappe.db.get_value("Customer", self.client, "customer_name") if self.client else None
		self.agreement_reference = f"M/s {client_name}" if client_name else self.agreement_reference
		service_types = ", ".join(row.engagement_type for row in self.services if row.engagement_type)
		parts = [client_name or self.client, service_types]
		self.engagement_name = " - ".join([p for p in parts if p])
