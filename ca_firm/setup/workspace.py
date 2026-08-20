import json

import frappe

WORKSPACE_NAME = "CA Firm"

# (section header, [(label, doctype), ...])
SECTIONS = [
	("Firm Profile", [
		("Company", "Company"),
		("Employee", "Employee"),
		("Designation", "Designation"),
	]),
	("Client Onboarding", [
		("Client Onboarding", "Client Onboarding"),
		("Clients", "Customer"),
		("Client Fee Arrangement", "Client Fee Arrangement"),
	]),
	("Client Engagement", [
		("Client Engagement", "Client Engagement"),
	]),
	("Statutory Audit - Planning", [
		("Statutory Audit Engagement", "Statutory Audit Engagement"),
		("Materiality Workings", "Materiality Workings"),
		("Understanding of the Entity", "Understanding of the Entity"),
		("Internal Control Evaluation", "Internal Control Evaluation"),
		("Risk Assessment", "Risk Assessment"),
		("Fraud Risk Assessment", "Fraud Risk Assessment"),
		("Going Concern Assessment", "Going Concern Assessment"),
		("Audit Strategy and Plan", "Audit Strategy and Plan"),
		("Audit Program Template", "Audit Program Template"),
		("Audit Program", "Audit Program"),
		("Sampling Worksheet", "Sampling Worksheet"),
		("Analytical Procedure", "Analytical Procedure"),
	]),
	("Statutory Audit - Execution", [
		("Audit Working Paper", "Audit Working Paper"),
		("Audit Procedure", "Audit Procedure"),
		("CAAT Test Template", "CAAT Test Template"),
		("CAAT Run", "CAAT Run"),
		("Checklist Template", "Checklist Template"),
		("Checklist Instance", "Checklist Instance"),
		("Confirmation Request", "Confirmation Request"),
		("Physical Verification", "Physical Verification"),
		("Subsequent Events Review", "Subsequent Events Review"),
		("Written Representation Letter", "Written Representation Letter"),
		("Audit Query", "Audit Query"),
		("Audit Finding", "Audit Finding"),
	]),
	("Statutory Audit - Review and Reporting", [
		("Review Note", "Review Note"),
		("Engagement Quality Control Review", "Engagement Quality Control Review"),
		("Management Letter", "Management Letter"),
		("Key Audit Matter", "Key Audit Matter"),
		("Audit Report Template", "Audit Report Template"),
		("Audit Opinion Paragraph", "Audit Opinion Paragraph"),
		("Audit Report", "Audit Report"),
		("Deliverable", "Deliverable"),
	]),
	("Other Assignment Modules", [
		("Tax Engagement", "Tax Engagement"),
		("Internal Audit Engagement", "Internal Audit Engagement"),
		("Review Engagement", "Review Engagement"),
		("Certification Engagement", "Certification Engagement"),
		("Inventory Audit Engagement", "Inventory Audit Engagement"),
		("Advisory Engagement", "Advisory Engagement"),
		("Company Secretarial Engagement", "Company Secretarial Engagement"),
		("Bookkeeping Engagement", "Bookkeeping Engagement"),
	]),
	("Regulatory and Standards", [
		("Applicable Law", "Applicable Law"),
		("Audit Standard", "Audit Standard"),
		("Regulatory Requirement", "Regulatory Requirement"),
		("Financial Statement Area", "Financial Statement Area"),
		("Assertion", "Assertion"),
		("Risk Category", "Risk Category"),
		("Audit Procedure Type", "Audit Procedure Type"),
	]),
]


def _build_content_and_shortcuts():
	content = []
	shortcuts = []
	idx = 0
	for header, items in SECTIONS:
		idx += 1
		content.append({
			"id": f"header-{idx}",
			"type": "header",
			"data": {"text": f"<span class=\"h4\"><b>{header}</b></span>", "col": 12},
		})
		for label, doctype in items:
			idx += 1
			content.append({"id": f"shortcut-{idx}", "type": "shortcut", "data": {"shortcut_name": label, "col": 3}})
			shortcuts.append({"label": label, "link_to": doctype, "type": "DocType", "doc_view": ""})
		idx += 1
		content.append({"id": f"spacer-{idx}", "type": "spacer", "data": {"col": 12}})
	return content, shortcuts


def create_workspace():
	# Rebuilt on every install/migrate so the workspace always matches the
	# app's current module structure, rather than drifting from source once
	# created (unlike master data, a stale workspace has no way to "catch up").
	if frappe.db.exists("Workspace", WORKSPACE_NAME):
		frappe.delete_doc("Workspace", WORKSPACE_NAME, force=True, ignore_permissions=True)
	content, shortcuts = _build_content_and_shortcuts()
	doc = frappe.new_doc("Workspace")
	doc.name = WORKSPACE_NAME
	doc.label = WORKSPACE_NAME
	doc.title = WORKSPACE_NAME
	doc.module = "CA Firm Setup"
	doc.public = 1
	doc.is_hidden = 0
	doc.icon = "list"
	doc.indicator_color = "blue"
	doc.sequence_id = 1.0
	doc.content = json.dumps(content)
	for sc in shortcuts:
		doc.append("shortcuts", sc)
	doc.insert(ignore_permissions=True)

	# Best-effort cache/sidebar-pin cleanup -- must never be allowed to raise
	# past this point, since the caller commits per-step and a failure here
	# would roll back the doc.insert() above along with it.
	try:
		frappe.delete_doc_if_exists("Workspace Sidebar", WORKSPACE_NAME, force=True)
		frappe.clear_cache()
	except Exception:
		frappe.log_error(title="CA Firm: workspace cache/sidebar cleanup failed (workspace itself was created)")
