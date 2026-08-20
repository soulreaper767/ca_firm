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

	def compute_mus_sample_size(self):
		self.reliability_factor = RELIABILITY_FACTORS.get(self.confidence_level, 3.00)
		tolerable = frappe.utils.flt(self.tolerable_misstatement)
		population = frappe.utils.flt(self.population_value)
		if tolerable and population:
			self.sample_size = int(-(-population * self.reliability_factor // tolerable))  # ceiling division
			self.sampling_interval = population / self.sample_size if self.sample_size else 0
