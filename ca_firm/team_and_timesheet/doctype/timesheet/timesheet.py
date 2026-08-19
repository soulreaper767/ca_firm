import frappe
from frappe.model.document import Document


class Timesheet(Document):
	def validate(self):
		self.compute_totals()

	def compute_totals(self):
		total = 0.0
		billable = 0.0
		for row in self.entries:
			hours = frappe.utils.flt(row.hours)
			total += hours
			if row.is_billable:
				billable += hours
		self.total_hours = total
		self.billable_hours = billable

	def on_submit(self):
		self.roll_up_to_audit_procedures()

	def roll_up_to_audit_procedures(self):
		for row in self.entries:
			if not row.audit_procedure:
				continue
			current = frappe.db.get_value("Audit Procedure", row.audit_procedure, "actual_hours") or 0
			frappe.db.set_value(
				"Audit Procedure", row.audit_procedure, "actual_hours",
				frappe.utils.flt(current) + frappe.utils.flt(row.hours),
			)
