import frappe
from frappe.model.document import Document


class ReviewMateriality(Document):
	def validate(self):
		self.materiality_amount = frappe.utils.flt(self.benchmark_amount) * frappe.utils.flt(self.percentage) / 100
