import frappe

AUDIT_REPORT_HTML = """
<div style="font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.5;">
	{% set eng = frappe.get_doc("Statutory Audit Engagement", doc.engagement) if doc.engagement else None %}
	{% set client_name = frappe.db.get_value("Customer", eng.client, "customer_name") if eng and eng.client else "" %}
	<h2 style="text-align:center;">INDEPENDENT AUDITOR'S REPORT</h2>
	<p style="text-align:center;">To the members of {{ client_name }}</p>
	<p style="text-align:center;"><b>Report on the Audit of the Financial Statements</b></p>

	<h4>Opinion</h4>
	<div>{{ doc.opinion_paragraph or '' }}</div>

	<h4>Basis for Opinion</h4>
	<div>{{ doc.basis_for_opinion or '' }}</div>

	{% if doc.key_audit_matters %}
	<h4>Key Audit Matters</h4>
	<p>Key audit matters are those matters that, in our professional judgment, were of most significance
	in our audit of the financial statements of the current period. These matters were addressed in the
	context of our audit of the financial statements as a whole, and in forming our opinion thereon,
	and we do not provide a separate opinion on these matters.</p>
	{% for row in doc.key_audit_matters %}
	<div style="margin-bottom: 10px;">
		{% set kam = frappe.get_doc("Key Audit Matter", row.key_audit_matter) %}
		<b>{{ kam.matter_title }}</b>
		<p><i>Why the matter was determined to be a key audit matter</i></p>
		<div>{{ kam.why_kam or '' }}</div>
		<p><i>How the matter was addressed in our audit</i></p>
		<div>{{ kam.how_addressed or '' }}</div>
	</div>
	{% endfor %}
	{% endif %}

	{% if doc.emphasis_of_matter %}
	<h4>Emphasis of Matter</h4>
	<div>{{ doc.emphasis_of_matter }}</div>
	{% endif %}

	{% if doc.other_matter %}
	<h4>Other Matter</h4>
	<div>{{ doc.other_matter }}</div>
	{% endif %}

	<h4>Responsibilities of Management and Board of Directors for the Financial Statements</h4>
	<div>{{ doc.responsibilities_of_management or '' }}</div>

	<h4>Auditor's Responsibilities for the Audit of the Financial Statements</h4>
	<div>{{ doc.responsibilities_of_auditor or '' }}</div>

	{% if doc.other_reporting_responsibilities %}
	<h4>Report on Other Legal and Regulatory Requirements</h4>
	<div>{{ doc.other_reporting_responsibilities }}</div>
	{% endif %}

	<div style="margin-top: 40px;">
		<table style="width:100%; border:none;">
			<tr>
				<td style="border:none; width:60%;"></td>
				<td style="border:none; text-align:center;">
					<div>{{ doc.engagement_partner_name or '' }}</div>
					<div>Engagement Partner</div>
					<div>ICAP Membership No: {{ doc.signing_partner_membership_no or '' }}</div>
				</td>
			</tr>
		</table>
		<p>{{ doc.place_of_signing or '' }}</p>
		<p>Date: {{ frappe.utils.formatdate(doc.report_date) if doc.report_date else '' }}</p>
	</div>
</div>
"""


def create_audit_report_print_format():
	name = "Audit Report - Standard Presentation"
	if frappe.db.exists("Print Format", name):
		return
	frappe.get_doc({
		"doctype": "Print Format",
		"name": name,
		"doc_type": "Audit Report",
		"module": "Statutory Audit",
		"print_format_type": "Jinja",
		"html": AUDIT_REPORT_HTML,
		"standard": "No",
		"custom_format": 1,
		"disabled": 0,
	}).insert(ignore_permissions=True)


def create_all():
	try:
		create_audit_report_print_format()
	except Exception:
		frappe.log_error(title="CA Firm: failed to create print formats")
