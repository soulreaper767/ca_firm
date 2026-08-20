import frappe
from frappe.model.document import Document

from ca_firm.utils.cross_reference import create_cross_reference


class InventoryCountSheet(Document):
	def validate(self):
		total = 0.0
		for item in self.items:
			item.variance = frappe.utils.flt(item.counted_quantity) - frappe.utils.flt(item.book_quantity)
			total += item.variance * frappe.utils.flt(item.unit_value)
		self.total_variance_value = total

	@frappe.whitelist()
	def flag_variance_to_audit(self):
		"""A material inventory count variance is exactly the kind of thing
		the statutory auditor for the same period needs to know about --
		it may point to a misstatement in the Inventory head they're
		relying on. Finds the Statutory Audit Engagement for the same
		client and financial year and raises a cross-reference against it."""
		if not self.total_variance_value:
			frappe.throw("This count sheet has no variance to flag.")

		client, financial_year = frappe.db.get_value(
			"Inventory Audit Engagement", self.engagement, ["client", "financial_year"]
		)
		if not client:
			frappe.throw("This count sheet's engagement has no client set.")

		audit_engagement = frappe.db.get_value(
			"Statutory Audit Engagement",
			{"client": client, "financial_year": financial_year},
			"name",
		)
		if not audit_engagement:
			frappe.throw(
				"No Statutory Audit Engagement found for this client and financial year to flag to."
			)

		create_cross_reference(
			source_doctype="Inventory Count Sheet",
			source_name=self.name,
			target_doctype="Statutory Audit Engagement",
			target_name=audit_engagement,
			relationship_type="Raises Audit Adjustment",
			client=client,
			linked_head=self.linked_head,
			remarks=f"Inventory Count Sheet {self.name} ({self.location or ''}) variance: "
			f"{frappe.utils.fmt_money(self.total_variance_value)}",
		)
		frappe.msgprint(f"Flagged to Statutory Audit Engagement {audit_engagement}.")
