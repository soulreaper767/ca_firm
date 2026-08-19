import frappe
from frappe.model.document import Document


class ChecklistInstance(Document):
	def validate(self):
		self.populate_from_template()
		self.compute_overall_status()

	def populate_from_template(self):
		if self.items or not self.checklist_template:
			return
		template = frappe.get_doc("Checklist Template", self.checklist_template)
		for row in template.items:
			self.append("items", {
				"item_no": row.item_no,
				"particular": row.particular,
				"reference": row.reference,
				"is_mandatory": row.is_mandatory,
				"status": "Pending",
			})

	def compute_overall_status(self):
		if self.items and all(row.status in ("Received", "Not Applicable", "Reviewed") for row in self.items):
			self.overall_status = "Completed"
			if not self.completion_date:
				self.completion_date = frappe.utils.today()
		else:
			self.overall_status = "In Progress"
