import frappe
from frappe.model.document import Document


class AuditAdjustment(Document):
	def validate(self):
		total_debit = sum(frappe.utils.flt(row.debit) for row in self.lines)
		total_credit = sum(frappe.utils.flt(row.credit) for row in self.lines)
		self.total_debit = total_debit
		self.total_credit = total_credit
		self.is_balanced = 1 if abs(total_debit - total_credit) < 0.01 else 0
