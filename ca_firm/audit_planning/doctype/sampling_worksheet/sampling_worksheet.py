import frappe
from frappe.model.document import Document


class SamplingWorksheet(Document):
	def validate(self):
		self.exceptions_noted = len([row for row in (self.items_selected or []) if row.exception_noted])
