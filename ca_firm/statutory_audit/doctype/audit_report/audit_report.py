import frappe
from frappe.model.document import Document

# Report Paragraph Type -> Audit Report field it feeds.
PARAGRAPH_TYPE_FIELD_MAP = {
	"Opinion - Unmodified": "opinion_paragraph",
	"Opinion - Qualified": "opinion_paragraph",
	"Opinion - Adverse": "opinion_paragraph",
	"Opinion - Disclaimer": "opinion_paragraph",
	"Basis for Opinion": "basis_for_opinion",
	"Basis for Qualified Opinion": "basis_for_opinion",
	"Basis for Adverse Opinion": "basis_for_opinion",
	"Basis for Disclaimer of Opinion": "basis_for_opinion",
	"Emphasis of Matter": "emphasis_of_matter",
	"Material Uncertainty Related to Going Concern": "emphasis_of_matter",
	"Other Matter": "other_matter",
	"Other Reporting Requirements (Fourth Schedule)": "other_reporting_responsibilities",
	"Responsibilities of Management": "responsibilities_of_management",
	"Responsibilities of Auditor": "responsibilities_of_auditor",
}


class AuditReport(Document):
	def validate(self):
		if self.report_template and not self._already_populated():
			self.pull_from_template()

	def _already_populated(self):
		return any(self.get(f) for f in set(PARAGRAPH_TYPE_FIELD_MAP.values()))

	@frappe.whitelist()
	def pull_from_template(self):
		if not self.report_template:
			frappe.throw("Select a Report Template first.")
		template = frappe.get_doc("Audit Report Template", self.report_template)
		context = self._build_context()
		for row in sorted(template.paragraphs, key=lambda r: r.sequence or 0):
			field = PARAGRAPH_TYPE_FIELD_MAP.get(row.paragraph_type)
			if not field or not row.audit_opinion_paragraph:
				continue
			text = frappe.db.get_value("Audit Opinion Paragraph", row.audit_opinion_paragraph, "paragraph_text")
			if not text:
				continue
			rendered = frappe.render_template(text, context)
			existing = self.get(field)
			self.set(field, (existing + "\n\n" + rendered) if existing else rendered)

	def _build_context(self):
		engagement = frappe.db.get_value(
			"Statutory Audit Engagement", self.engagement, ["client", "financial_year", "period_end"], as_dict=True
		) or {}
		client_name = None
		if engagement.get("client"):
			client_name = frappe.db.get_value("Customer", engagement["client"], "customer_name")
		overall_materiality = frappe.db.get_value(
			"Materiality Workings", {"engagement": self.engagement}, "overall_materiality"
		)
		return {
			"client_name": client_name or "",
			"financial_year": engagement.get("financial_year") or "",
			"period_end": frappe.utils.formatdate(engagement.get("period_end")) if engagement.get("period_end") else "",
			"framework": "",
			"overall_materiality": frappe.utils.fmt_money(overall_materiality, currency="PKR") if overall_materiality else "",
		}
