import frappe
from frappe.model.document import Document


class SamplingWorksheet(Document):
	def validate(self):
		self.exceptions_found = sum(1 for row in self.sample_items if row.exception_noted)
