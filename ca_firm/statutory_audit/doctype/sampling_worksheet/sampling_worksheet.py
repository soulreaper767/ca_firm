import frappe
from frappe.model.document import Document

# Poisson reliability factors for zero expected misstatements, per ISA 530 /
# standard MUS practice -- publicly documented statistical constants, not
# proprietary to any vendor.
RELIABILITY_FACTORS = {
	"90%": 2.31,
	"95%": 3.00,
	"99%": 4.61,
}


class SamplingWorksheet(Document):
	def validate(self):
		self.exceptions_found = sum(1 for row in self.sample_items if row.exception_noted)
		if self.sampling_method == "Statistical - Monetary Unit Sampling":
			self.compute_mus_sample_size()
		self.check_extended_testing_trigger()

	def compute_mus_sample_size(self):
		self.reliability_factor = RELIABILITY_FACTORS.get(self.confidence_level, 3.00)
		tolerable = frappe.utils.flt(self.tolerable_misstatement)
		population = frappe.utils.flt(self.population_value)
		if tolerable and population:
			self.sample_size = int(-(-population * self.reliability_factor // tolerable))  # ceiling division
			self.sampling_interval = population / self.sample_size if self.sample_size else 0

	def check_extended_testing_trigger(self):
		"""ISA 530.14: if the sample results indicate the population may be
		misstated beyond what's tolerable, the auditor should consider
		extending the sample or performing alternative procedures. This just
		flags it and logs the trigger -- the actual extended worksheet is a
		normal follow-up record the preparer creates, linked back via
		extended_from."""
		was_flagged = self.requires_extended_testing
		self.requires_extended_testing = 1 if self.exceptions_found > frappe.utils.cint(self.tolerable_exception_count) else 0
		if self.requires_extended_testing and not was_flagged:
			frappe.msgprint(
				f"{self.exceptions_found} exception(s) found, exceeding the tolerable count of "
				f"{self.tolerable_exception_count}. Consider extending the sample or reassessing "
				f"the risk of material misstatement for this area.",
				indicator="orange", alert=True,
			)

	def on_update(self):
		if self.requires_extended_testing:
			self._log_revision()

	def _log_revision(self):
		if frappe.db.exists("Engagement Revision Log", {
			"engagement": self.engagement, "reference_doctype": "Sampling Worksheet", "reference_name": self.name,
		}):
			return
		revision_type = frappe.db.get_value(
			"Revision Type", "Sample Extended - Exceptions Exceeded Tolerable Rate", "name"
		)
		frappe.get_doc({
			"doctype": "Engagement Revision Log",
			"engagement": self.engagement,
			"revision_date": frappe.utils.today(),
			"revision_type": revision_type,
			"trigger_description": self.revision_reason or (
				f"{self.exceptions_found} exception(s) found against a tolerable count of "
				f"{self.tolerable_exception_count} in sampling for {self.fs_area or 'this area'}."
			),
			"after_state": "Flagged as requiring extended testing / reassessment",
			"reference_doctype": "Sampling Worksheet",
			"reference_name": self.name,
		}).insert(ignore_permissions=True)
