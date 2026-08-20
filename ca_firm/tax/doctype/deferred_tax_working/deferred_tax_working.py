import frappe
from frappe.model.document import Document


class DeferredTaxWorking(Document):
	def validate(self):
		total_dta = 0.0
		total_dtl = 0.0
		for item in self.items:
			item.temporary_difference = frappe.utils.flt(item.carrying_value) - frappe.utils.flt(item.tax_base)
			amount = abs(item.temporary_difference) * frappe.utils.flt(item.tax_rate) / 100
			if item.classification == "Taxable Temporary Difference":
				item.deferred_tax_liability = amount
				item.deferred_tax_asset = 0
				total_dtl += amount
			else:
				item.deferred_tax_asset = amount
				item.deferred_tax_liability = 0
				total_dta += amount

		self.total_deferred_tax_asset = total_dta
		self.total_deferred_tax_liability = total_dtl
		self.net_deferred_tax = total_dtl - total_dta

		closing = self.net_deferred_tax
		oci_movement = frappe.utils.flt(self.movement_recognized_in_oci)
		self.movement_recognized_in_pl = (
			closing - frappe.utils.flt(self.opening_net_deferred_tax) - oci_movement
		)
