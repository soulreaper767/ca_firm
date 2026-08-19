import frappe
from frappe.model.document import Document


class AnalyticalProcedure(Document):
	def validate(self):
		self.compute_variance()

	def compute_variance(self):
		current = frappe.utils.flt(self.current_year_amount)
		expected = frappe.utils.flt(self.expected_amount)
		self.variance_amount = current - expected
		self.variance_percent = (
			(self.variance_amount / expected * 100.0) if expected else 0.0
		)
		threshold = frappe.utils.flt(self.threshold_percent)
		self.exceeds_threshold = 1 if abs(self.variance_percent) > threshold else 0
