import frappe
from frappe.model.document import Document


class TrialBalance(Document):
	def validate(self):
		self.auto_map_heads()
		total_debit = sum(frappe.utils.flt(row.current_year_debit) for row in self.entries)
		total_credit = sum(frappe.utils.flt(row.current_year_credit) for row in self.entries)
		self.total_debit = total_debit
		self.total_credit = total_credit
		self.is_balanced = 1 if abs(total_debit - total_credit) < 0.01 else 0

	def auto_map_heads(self):
		"""Fill mapped_head from the client's standing Chart of Accounts Mapping
		when a row's account code matches and no head has been set yet."""
		client = frappe.db.get_value("Statutory Audit Engagement", self.engagement, "client")
		if not client:
			return
		mapping = {
			row.client_account_code: row.mapped_head
			for row in frappe.get_all(
				"Client Chart of Accounts Mapping",
				filters={"client": client, "is_active": 1},
				fields=["client_account_code", "mapped_head"],
			)
			if row.client_account_code
		}
		for row in self.entries:
			if not row.mapped_head and row.client_account_code in mapping:
				row.mapped_head = mapping[row.client_account_code]
