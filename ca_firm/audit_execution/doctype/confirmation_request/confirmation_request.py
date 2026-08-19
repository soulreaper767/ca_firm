import frappe
from frappe.model.document import Document


class ConfirmationRequest(Document):
	def validate(self):
		if self.response_received:
			self.difference_amount = frappe.utils.flt(self.amount_as_per_confirmation) - frappe.utils.flt(
				self.amount_as_per_books
			)
			if not self.difference_amount:
				self.difference_reconciled = 1
