import frappe
from frappe.model.document import Document


class CAATRun(Document):
	def validate(self):
		self.exceptions_count = len(self.exceptions or [])
