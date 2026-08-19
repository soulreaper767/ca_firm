import frappe
from frappe.model.document import Document


class CaatRun(Document):
	def validate(self):
		self.exceptions_found = len(self.exceptions or [])
