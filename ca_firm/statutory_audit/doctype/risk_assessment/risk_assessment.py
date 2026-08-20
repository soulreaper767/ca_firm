import frappe
from frappe.model.document import Document

# Simple 4x4 risk matrix (Rating Scale: Low/Medium/High/Critical). Combines
# inherent and control risk into an overall risk of material misstatement,
# erring toward the higher of the two inputs rather than averaging, since
# that's the conservative convention auditors use.
RATING_ORDER = ["Low", "Medium", "High", "Critical"]


class RiskAssessment(Document):
	def validate(self):
		self.risk_of_material_misstatement = self.compute_rmm()

	def compute_rmm(self):
		if not self.inherent_risk or not self.control_risk:
			return None
		try:
			ir_idx = RATING_ORDER.index(self.inherent_risk)
			cr_idx = RATING_ORDER.index(self.control_risk)
		except ValueError:
			# a custom rating value outside the standard four was added to
			# the Rating Scale master -- fall back to whichever was entered
			# for inherent risk rather than guessing at its position.
			return self.inherent_risk
		return RATING_ORDER[max(ir_idx, cr_idx)]
