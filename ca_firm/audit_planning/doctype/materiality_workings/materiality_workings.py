import frappe
from frappe.model.document import Document


class MaterialityWorkings(Document):
	def validate(self):
		self.compute_materiality()

	def compute_materiality(self):
		benchmark_amount = frappe.utils.flt(self.benchmark_amount)
		self.overall_materiality = benchmark_amount * frappe.utils.flt(self.materiality_percent) / 100.0
		self.performance_materiality = (
			self.overall_materiality * frappe.utils.flt(self.performance_materiality_percent) / 100.0
		)
		self.clearly_trivial_threshold = (
			self.overall_materiality * frappe.utils.flt(self.clearly_trivial_percent) / 100.0
		)
