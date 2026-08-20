import frappe
from frappe.model.document import Document


class StatutoryAuditEngagement(Document):
	def validate(self):
		self.validate_eqcr()
		self.compute_completion_percent()

	def validate_eqcr(self):
		if self.is_eqcr_required and not self.eqcr_partner:
			frappe.msgprint(
				"EQCR is marked as required for this engagement but no EQCR Partner has been assigned.",
				indicator="orange",
				alert=True,
			)

	def compute_completion_percent(self):
		total = frappe.db.count("Audit Procedure", {"engagement": self.name})
		if not total:
			self.completion_percent = 0
			return
		completed = frappe.db.count("Audit Procedure", {"engagement": self.name, "status": "Completed"})
		self.completion_percent = (completed / total) * 100

	def on_update(self):
		if self.status == "Completed" and not self.actual_completion_date:
			self.db_set("actual_completion_date", frappe.utils.today())
		self.log_team_changes()

	def log_team_changes(self):
		"""Every add/remove/role change on the engagement team is written to
		Team Assignment History -- "A was given assignment X at this time,
		who changed it" -- rather than relying on generic field-level
		version diffs to answer that question."""
		before = self.get_doc_before_save()
		before_team = {row.staff_member: row.role_in_engagement for row in (before.engagement_team if before else [])}
		after_team = {row.staff_member: row.role_in_engagement for row in self.engagement_team}

		for staff_member, role in after_team.items():
			if staff_member not in before_team:
				self._add_history(staff_member, "Assigned", role_in_engagement=role)
			elif before_team[staff_member] != role:
				self._add_history(staff_member, "Role Changed", role_in_engagement=role, previous_role=before_team[staff_member])

		for staff_member, role in before_team.items():
			if staff_member not in after_team:
				self._add_history(staff_member, "Removed", role_in_engagement=role)

	def _add_history(self, staff_member, action, role_in_engagement=None, previous_role=None):
		frappe.get_doc({
			"doctype": "Team Assignment History",
			"engagement": self.name,
			"staff_member": staff_member,
			"action": action,
			"role_in_engagement": role_in_engagement,
			"previous_role": previous_role,
			"changed_by_user": frappe.session.user,
		}).insert(ignore_permissions=True)
