import frappe
from frappe.model.document import Document


class CAATRun(Document):
	def validate(self):
		self.exceptions_found = len(self.exceptions or [])
