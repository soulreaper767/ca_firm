import frappe
from frappe.model.document import Document

# Standard risk-of-material-misstatement matrix: inherent risk x control risk.
RMM_MATRIX = {
	("Low", "Low"): "Low",
	("Low", "Medium"): "Low",
	("Low", "High"): "Medium",
	("Medium", "Low"): "Low",
	("Medium", "Medium"): "Medium",
	("Medium", "High"): "High",
	("High", "Low"): "Medium",
	("High", "Medium"): "High",
	("High", "High"): "High",
}


class RiskAssessment(Document):
	def validate(self):
		self.compute_rmm()

	def compute_rmm(self):
		if self.inherent_risk and self.control_risk:
			self.risk_of_material_misstatement = RMM_MATRIX.get(
				(self.inherent_risk, self.control_risk), self.risk_of_material_misstatement
			)
		if self.risk_of_material_misstatement == "High" or self.fraud_related:
			self.is_significant_risk = 1
