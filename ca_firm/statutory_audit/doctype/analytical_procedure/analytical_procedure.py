import frappe
from frappe.model.document import Document


class AnalyticalProcedure(Document):
	def validate(self):
		expected = frappe.utils.flt(self.expected_amount)
		actual = frappe.utils.flt(self.current_year_amount)
		if expected:
			self.variance_amount = actual - expected
			self.variance_percent = (self.variance_amount / expected) * 100 if expected else 0
			self.exceeds_threshold = 1 if abs(self.variance_percent) > frappe.utils.flt(self.threshold_percent) else 0
