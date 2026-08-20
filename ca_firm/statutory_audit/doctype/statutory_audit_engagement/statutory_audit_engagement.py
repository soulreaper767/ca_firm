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

	@frappe.whitelist()
	def roll_forward(self, client_engagement, financial_year, period_start=None, period_end=None):
		"""Create next year's engagement from this one, instead of starting a
		blank form: team, EQCR/group settings and component auditor details
		carry over as defaults (all editable on the new record), a fresh
		Materiality Workings is pre-filled with the same benchmark/percentages
		(the amount itself must be re-entered against the new year's figures),
		and the current Risk Assessment rows are copied forward flagged for
		reassessment -- ISA 315's expectation that prior-year understanding
		informs, but does not replace, the current year's risk work."""
		new_engagement = frappe.new_doc("Statutory Audit Engagement")
		new_engagement.client = self.client
		new_engagement.client_engagement = client_engagement
		new_engagement.financial_year = financial_year
		new_engagement.period_start = period_start
		new_engagement.period_end = period_end
		new_engagement.engagement_partner = self.engagement_partner
		new_engagement.engagement_manager = self.engagement_manager
		new_engagement.job_incharge = self.job_incharge
		new_engagement.is_eqcr_required = self.is_eqcr_required
		new_engagement.eqcr_partner = self.eqcr_partner
		new_engagement.component_auditor_role = self.component_auditor_role
		new_engagement.component_auditor_details = self.component_auditor_details
		new_engagement.group_structure = self.group_structure
		new_engagement.rolled_forward_from = self.name
		new_engagement.status = "Draft"
		for row in self.engagement_team:
			new_engagement.append("engagement_team", {
				"staff_member": row.staff_member,
				"designation": row.designation,
				"role_in_engagement": row.role_in_engagement,
			})
		new_engagement.insert(ignore_permissions=True, ignore_mandatory=True)

		self._copy_materiality_basis(new_engagement.name)
		self._copy_risk_assessments(new_engagement.name)
		return new_engagement.name

	def _copy_materiality_basis(self, new_engagement_name):
		current = frappe.get_all(
			"Materiality Workings", filters={"engagement": self.name, "is_current": 1},
			fields=["benchmark", "materiality_percent", "performance_materiality_percent", "clearly_trivial_percent"],
			limit=1,
		)
		if not current:
			return
		prior = current[0]
		frappe.get_doc({
			"doctype": "Materiality Workings",
			"engagement": new_engagement_name,
			"benchmark": prior.benchmark,
			"benchmark_amount": 0,
			"materiality_percent": prior.materiality_percent,
			"performance_materiality_percent": prior.performance_materiality_percent,
			"clearly_trivial_percent": prior.clearly_trivial_percent,
			"rationale": "Carried forward from prior year engagement -- update the benchmark amount for the current year.",
		}).insert(ignore_permissions=True, ignore_mandatory=True)

	def _copy_risk_assessments(self, new_engagement_name):
		prior_risks = frappe.get_all(
			"Risk Assessment", filters={"engagement": self.name},
			fields=["fs_area", "assertion", "risk_category", "risk_description",
			        "inherent_risk", "control_risk", "planned_response"],
		)
		for row in prior_risks:
			frappe.get_doc({
				"doctype": "Risk Assessment",
				"engagement": new_engagement_name,
				"fs_area": row.fs_area,
				"assertion": row.assertion,
				"risk_category": row.risk_category,
				"risk_description": f"{row.risk_description} (carried forward from prior year -- reassess)",
				"inherent_risk": row.inherent_risk,
				"control_risk": row.control_risk,
				"planned_response": row.planned_response,
			}).insert(ignore_permissions=True, ignore_mandatory=True)
