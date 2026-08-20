import frappe
from frappe.model.document import Document


class MaterialityWorkings(Document):
	def validate(self):
		self.compute_thresholds()
		if self.is_new():
			self.set_revision_chain()

	def compute_thresholds(self):
		amount = frappe.utils.flt(self.benchmark_amount)
		self.overall_materiality = amount * frappe.utils.flt(self.materiality_percent) / 100
		self.performance_materiality = self.overall_materiality * frappe.utils.flt(self.performance_materiality_percent) / 100
		self.clearly_trivial_threshold = self.overall_materiality * frappe.utils.flt(self.clearly_trivial_percent) / 100

	def set_revision_chain(self):
		"""Every Materiality Workings for an engagement stays on file -- a
		revision doesn't overwrite the prior one, it supersedes it, so the
		full history of how materiality moved through the engagement (and
		why) is preserved."""
		previous = frappe.get_all(
			"Materiality Workings",
			filters={"engagement": self.engagement, "is_current": 1},
			fields=["name"], limit=1,
		)
		if previous:
			self.supersedes = previous[0].name
			self.revision_no = frappe.utils.cint(
				frappe.db.get_value("Materiality Workings", previous[0].name, "revision_no")
			) + 1
			frappe.db.set_value("Materiality Workings", previous[0].name, "is_current", 0)
		else:
			self.revision_no = 1
		self.is_current = 1

	def on_update(self):
		if self.revision_no and self.revision_no > 1:
			self._log_revision()

	def _log_revision(self):
		if frappe.db.exists("Engagement Revision Log", {
			"engagement": self.engagement, "reference_doctype": "Materiality Workings", "reference_name": self.name,
		}):
			return
		frappe.get_doc({
			"doctype": "Engagement Revision Log",
			"engagement": self.engagement,
			"revision_date": frappe.utils.today(),
			"revision_type": self.revision_trigger,
			"trigger_description": self.revision_reason,
			"before_state": f"Overall materiality (rev {self.revision_no - 1}): see {self.supersedes}",
			"after_state": f"Overall materiality (rev {self.revision_no}): {self.overall_materiality}",
			"reference_doctype": "Materiality Workings",
			"reference_name": self.name,
			"revised_by": self.prepared_by,
		}).insert(ignore_permissions=True)
