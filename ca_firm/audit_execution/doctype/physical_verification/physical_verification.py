import frappe
from frappe.model.document import Document


class PhysicalVerification(Document):
	def validate(self):
		has_discrepancy = False
		for row in self.items_verified or []:
			row.variance = frappe.utils.flt(row.physical_quantity) - frappe.utils.flt(row.book_quantity)
			if row.variance:
				has_discrepancy = True
		if has_discrepancy:
			self.discrepancies_noted = 1
