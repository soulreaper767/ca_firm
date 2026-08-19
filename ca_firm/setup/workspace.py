import json

import frappe

WORKSPACE_NAME = "CA Firm"

# (section header, [(label, doctype), ...])
SECTIONS = [
	("Firm & People", [
		("Company", "Company"),
		("Employee", "Employee"),
		("Designation", "Designation"),
		("Audit Standard", "Audit Standard"),
		("Financial Statement Area", "Financial Statement Area"),
		("Assertion", "Assertion"),
		("Risk Category", "Risk Category"),
		("Industry Type", "Industry Type"),
		("Applicable Law", "Applicable Law"),
		("Audit Procedure Type", "Audit Procedure Type"),
	]),
	("Clients", [
		("Customer", "Customer"),
		("Customer Group", "Customer Group"),
		("Client Contact", "Client Contact"),
		("Related Party", "Related Party"),
		("Client Team Assignment", "Client Team Assignment"),
		("Client Fee Arrangement", "Client Fee Arrangement"),
	]),
	("Engagement Management", [
		("Engagement", "Engagement"),
		("Client Acceptance and Continuance", "Client Acceptance and Continuance"),
		("Independence Declaration", "Independence Declaration"),
		("Engagement Letter", "Engagement Letter"),
		("Engagement Quality Control Review", "Engagement Quality Control Review"),
		("Fraud Risk Assessment", "Fraud Risk Assessment"),
		("Communication with TCWG", "Communication with TCWG"),
	]),
	("Audit Planning", [
		("Materiality Workings", "Materiality Workings"),
		("Understanding of the Entity", "Understanding of the Entity"),
		("Internal Control Evaluation", "Internal Control Evaluation"),
		("Risk Assessment", "Risk Assessment"),
		("Audit Strategy and Plan", "Audit Strategy and Plan"),
		("Audit Program Template", "Audit Program Template"),
		("Audit Program", "Audit Program"),
		("Sampling Worksheet", "Sampling Worksheet"),
		("Analytical Procedure", "Analytical Procedure"),
		("Going Concern Assessment", "Going Concern Assessment"),
	]),
	("Audit Execution", [
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
	("Financial Statement Grouping", [
		("Trial Balance", "Trial Balance"),
		("Client Chart of Accounts Mapping", "Client Chart of Accounts Mapping"),
		("Chart of Accounts Head", "Chart of Accounts Head"),
		("FS Line Item", "FS Line Item"),
		("Client Financial Statement Template", "Client Financial Statement Template"),
	]),
	("Review and Quality Control", [
		("Review Note", "Review Note"),
	]),
	("Reporting", [
		("Management Letter", "Management Letter"),
		("Key Audit Matter", "Key Audit Matter"),
		("Audit Report", "Audit Report"),
		("Audit Report Template", "Audit Report Template"),
		("Audit Opinion Paragraph", "Audit Opinion Paragraph"),
		("Deliverable", "Deliverable"),
	]),
	("Team and Timesheet", [
		("Timesheet", "Timesheet"),
	]),
	("Quality Control Review (ICAP)", [
		("Firm Quality Control Policy", "Firm Quality Control Policy"),
		("QCR Review", "QCR Review"),
		("QCR Finding", "QCR Finding"),
	]),
	("Regulatory Compliance", [
		("Regulatory Requirement", "Regulatory Requirement"),
		("Law Section", "Law Section"),
		("Rate Schedule", "Rate Schedule"),
		("Financial Metric", "Financial Metric"),
		("Industry Benchmark", "Industry Benchmark"),
	]),
	("Configurable Lists", [
		("Rating Scale", "Rating Scale"),
		("Priority Level", "Priority Level"),
		("Entity Type", "Entity Type"),
		("Entity Size Category", "Entity Size Category"),
		("Engagement Type", "Engagement Type"),
		("Opinion Type", "Opinion Type"),
		("Finding Category", "Finding Category"),
		("Deliverable Type", "Deliverable Type"),
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
