import frappe
from frappe.model.document import Document


class ClientOnboarding(Document):
	def validate(self):
		if self.client_name:
			self.agreement_addressee = f"M/s {self.client_name}"

	def on_submit(self):
		customer = self.get_or_create_customer()
		self.create_fee_arrangement(customer)
		self.db_set("onboarded_client", customer.name)
		self.db_set("status", "Onboarded")

	def get_or_create_customer(self):
		if self.existing_client:
			return frappe.get_doc("Customer", self.existing_client)

		customer = frappe.new_doc("Customer")
		customer.customer_name = self.client_name
		customer.customer_type = "Company"
		customer.customer_group = self._default("Customer Group", "All Customer Groups")
		customer.territory = self._default("Territory", "All Territories")
		customer.tax_id = self.ntn
		customer.industry = self.industry
		customer.entity_type = self.entity_type
		customer.entity_size_category = self.entity_size_category
		customer.client_relationship_status = "Active"
		customer.is_listed_entity = self.is_listed_entity
		customer.is_public_interest_entity = self.is_public_interest_entity
		customer.cuin = self.cuin
		customer.strn = self.strn
		customer.date_of_incorporation = self.date_of_incorporation
		customer.financial_year_end = self._financial_year_end_value()
		customer.engagement_partner = self.engagement_partner
		customer.relationship_manager = self.relationship_manager
		# ignore_mandatory as a safety net: if the standard "All Customer
		# Groups"/"All Territories" records don't exist on this site for some
		# reason, a missing group/territory can be fixed up on the Customer
		# afterwards -- it shouldn't block the whole onboarding submission.
		customer.insert(ignore_permissions=True, ignore_mandatory=True)
		return customer

	def _default(self, doctype, name):
		return name if frappe.db.exists(doctype, name) else None

	def _financial_year_end_value(self):
		# Customer.financial_year_end is a plain Select (30 June/31 December/
		# 31 March/Other); this form links to the "Financial Year End
		# Pattern" master for the same options so it can stay editable, so
		# just pass the link value straight through -- the option text is
		# identical either way.
		return self.financial_year_end

	def create_fee_arrangement(self, customer):
		if not self.fee_amount:
			return
		frappe.get_doc({
			"doctype": "Client Fee Arrangement",
			"client": customer.name,
			"fee_amount": self.fee_amount,
			"billing_frequency": self.billing_frequency or self._default("Billing Frequency", "Per Engagement"),
			"start_date": self.target_start_date or frappe.utils.today(),
			"status": "Active",
			"agreed_by": self.engagement_partner,
			"notes": f"Created from Client Onboarding {self.name}",
		}).insert(ignore_permissions=True)
