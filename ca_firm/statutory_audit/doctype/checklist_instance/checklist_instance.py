import frappe
from frappe.model.document import Document


class ChecklistInstance(Document):
	def validate(self):
		if self.template and not self.items:
			self.populate_from_template()
		self.recompute_counts()

	@frappe.whitelist()
	def populate_from_template(self):
		"""Pull items from the template and auto-decide is_applicable per item
		against this engagement's client profile (entity size, listed/PIE
		status, industry) -- the "what-if" behaviour: a Small-Sized Company
		checklist item stays unticked-and-hidden-from-scope for a Large-Sized
		Company engagement, a listed-only item is skipped for an unlisted
		client, etc. Preparers can still override is_applicable by hand
		afterwards for judgment calls the rules can't capture."""
		if not self.template:
			return
		profile = self._engagement_profile()
		template = frappe.get_doc("Checklist Template", self.template)
		self.items = []
		for row in template.items:
			self.append("items", {
				"item_no": row.item_no,
				"particular": row.particular,
				"is_mandatory": row.is_mandatory,
				"is_applicable": 1 if self._item_applies(row, profile) else 0,
			})

	def _engagement_profile(self):
		if not self.engagement:
			return {}
		return frappe.db.get_value(
			"Statutory Audit Engagement", self.engagement,
			["entity_size_category", "is_listed_entity", "is_public_interest_entity", "industry"],
			as_dict=True,
		) or {}

	def _item_applies(self, row, profile):
		if row.applies_to_entity_size and row.applies_to_entity_size != profile.get("entity_size_category"):
			return False
		if row.applies_if_listed_only and not profile.get("is_listed_entity"):
			return False
		if row.applies_if_pie_only and not profile.get("is_public_interest_entity"):
			return False
		if row.applies_to_industry and row.applies_to_industry != profile.get("industry"):
			return False
		return True

	def recompute_counts(self):
		self.total_items = len(self.items)
		self.applicable_items = sum(1 for row in self.items if row.is_applicable)
		self.completed_items = sum(1 for row in self.items if row.is_applicable and row.is_complete)
