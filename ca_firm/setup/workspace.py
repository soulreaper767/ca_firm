import json

import frappe

TOP_WORKSPACE = "CA Firm"

# (workspace_name, module, [(section_header, [(label, doctype), ...]), ...])
# Each becomes its own Workspace document nested under "CA Firm" via
# parent_page, so it shows as a real main-menu item with its own sidebar
# entry -- not just a section on one long page. Within a workspace, section
# headers act as the sub-menu grouping (e.g. Statutory Audit's Planning/
# Execution/Review split).
CHILD_WORKSPACES = [
	("Firm Profile", "CA Firm Setup", [
		("Firm & Staff", [
			("Company", "Company"),
			("Employee", "Employee"),
			("Designation", "Designation"),
		]),
	]),
	("Client Onboarding", "Client Management", [
		("Onboarding", [
			("Client Onboarding", "Client Onboarding"),
			("Clients", "Customer"),
			("Client Fee Arrangement", "Client Fee Arrangement"),
		]),
		("Client Records", [
			("Permanent File Document", "Permanent File Document"),
			("Group Structure", "Group Structure"),
		]),
	]),
	("Client Engagement", "Engagement Management", [
		("Agreements", [
			("Client Engagement", "Client Engagement"),
		]),
		("Cross-Module Links", [
			("Engagement Cross Reference", "Engagement Cross Reference"),
			("Cross Module Linkages", "Cross Module Linkages", "Report"),
			("Cross Reference Type", "Cross Reference Type"),
		]),
	]),
	("Statutory Audit", "Statutory Audit", [
		("Planning", [
			("Statutory Audit Engagement", "Statutory Audit Engagement"),
			("Trial Balance", "Trial Balance"),
			("Client Chart of Accounts Mapping", "Client Chart of Accounts Mapping"),
			("Chart of Accounts Head", "Chart of Accounts Head"),
			("FS Line Item", "FS Line Item"),
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
		("Execution", [
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
			("Audit Adjustment", "Audit Adjustment"),
			("Consolidation Adjustment", "Consolidation Adjustment"),
		]),
		("Review and Reporting", [
			("Review Note", "Review Note"),
			("Engagement Quality Control Review", "Engagement Quality Control Review"),
			("Engagement Revision Log", "Engagement Revision Log"),
			("Management Letter", "Management Letter"),
			("Key Audit Matter", "Key Audit Matter"),
			("Audit Report Template", "Audit Report Template"),
			("Audit Opinion Paragraph", "Audit Opinion Paragraph"),
			("Audit Report", "Audit Report"),
			("Deliverable", "Deliverable"),
		]),
		("Team Management and Reports", [
			("My Engagements Overview", "My Engagements Overview", "Report"),
			("Team Allocation Overview", "Team Allocation Overview", "Report"),
			("Staff Workload", "Staff Workload", "Report"),
			("Daily Status Report", "Daily Status Report"),
			("Team Assignment History", "Team Assignment History"),
			("Lead Schedule", "Lead Schedule", "Report"),
			("PBC Status", "PBC Status", "Report"),
			("Materiality Summary", "Materiality Summary", "Report"),
			("Risk Register", "Risk Register", "Report"),
			("Audit Findings Register", "Audit Findings Register", "Report"),
			("Checklist Completion Status", "Checklist Completion Status", "Report"),
			("Engagement Status Report", "Engagement Status Report", "Report"),
		]),
	]),
	("Tax", "Tax", [
		("Tax", [
			("Tax Engagement", "Tax Engagement"),
			("Tax Return", "Tax Return"),
			("Tax Computation", "Tax Computation"),
			("Tax Notice", "Tax Notice"),
		]),
		("Reports", [
			("Tax Filing Status", "Tax Filing Status", "Report"),
			("Tax Notices Outstanding", "Tax Notices Outstanding", "Report"),
		]),
		("Setup", [
			("Tax Return Type", "Tax Return Type"),
			("Tax Notice Type", "Tax Notice Type"),
			("Rate Schedule", "Rate Schedule"),
		]),
	]),
	("Internal Audit", "Internal Audit", [
		("Internal Audit", [
			("Internal Audit Engagement", "Internal Audit Engagement"),
			("Internal Audit Plan", "Internal Audit Plan"),
			("Internal Audit Procedure", "Internal Audit Procedure"),
			("Internal Audit Observation", "Internal Audit Observation"),
		]),
		("Reports", [
			("Internal Audit Findings Register", "Internal Audit Findings Register", "Report"),
			("Internal Audit Action Tracker", "Internal Audit Action Tracker", "Report"),
		]),
		("Setup", [
			("Internal Audit Area", "Internal Audit Area"),
		]),
	]),
	("Review Engagements", "Review Engagements", [
		("Review Engagements", [
			("Review Engagement", "Review Engagement"),
			("Review Materiality", "Review Materiality"),
			("Review Procedure", "Review Procedure"),
		]),
		("Reports", [
			("Review Matters Noted Register", "Review Matters Noted Register", "Report"),
		]),
	]),
	("Certification Engagements", "Certification Engagements", [
		("Certification Engagements", [
			("Certification Engagement", "Certification Engagement"),
			("Certification Procedure", "Certification Procedure"),
			("Certificate Issued", "Certificate Issued"),
		]),
		("Reports", [
			("Certificates Issued Register", "Certificates Issued Register", "Report"),
		]),
		("Setup", [
			("Certificate Type", "Certificate Type"),
		]),
	]),
	("Inventory Audit", "Inventory Audit", [
		("Inventory Audit", [
			("Inventory Audit Engagement", "Inventory Audit Engagement"),
			("Inventory Count Sheet", "Inventory Count Sheet"),
		]),
		("Reports", [
			("Inventory Variance Summary", "Inventory Variance Summary", "Report"),
		]),
	]),
	("Advisory", "Advisory", [
		("Advisory", [("Advisory Engagement", "Advisory Engagement")]),
	]),
	("Company Secretarial", "Company Secretarial", [
		("Company Secretarial", [
			("Company Secretarial Engagement", "Company Secretarial Engagement"),
			("Statutory Filing", "Statutory Filing"),
		]),
		("Setup", [
			("Statutory Filing Type", "Statutory Filing Type"),
		]),
	]),
	("Bookkeeping and Accounting", "Bookkeeping and Accounting", [
		("Bookkeeping", [
			("Bookkeeping Engagement", "Bookkeeping Engagement"),
			("Bookkeeping Task", "Bookkeeping Task"),
		]),
		("Setup", [
			("Bookkeeping Task Type", "Bookkeeping Task Type"),
		]),
	]),
	("General Assignments", "General Assignments", [
		("General Assignments", [
			("General Assignment", "General Assignment"),
		]),
	]),
	("Regulatory and Standards", "CA Firm Setup", [
		("Reference Library", [
			("Applicable Law", "Applicable Law"),
			("Audit Standard", "Audit Standard"),
			("Regulatory Requirement", "Regulatory Requirement"),
			("Financial Statement Area", "Financial Statement Area"),
			("Assertion", "Assertion"),
			("Risk Category", "Risk Category"),
			("Audit Procedure Type", "Audit Procedure Type"),
		]),
	]),
]


def _workspace_route(name):
	return name.lower().replace(" ", "-")


def _build_content_and_shortcuts(sections):
	content = []
	shortcuts = []
	idx = 0
	for header, items in sections:
		idx += 1
		content.append({
			"id": f"header-{idx}",
			"type": "header",
			"data": {"text": f"<span class=\"h4\"><b>{header}</b></span>", "col": 12},
		})
		for item in items:
			# (label, link_to) for a DocType shortcut, (label, link_to,
			# "Report") for a Script Report shortcut, or (label, url, "URL")
			# to jump to another page (e.g. a sibling workspace).
			label, link_to = item[0], item[1]
			link_type = item[2] if len(item) > 2 else "DocType"
			idx += 1
			content.append({"id": f"shortcut-{idx}", "type": "shortcut", "data": {"shortcut_name": label, "col": 3}})
			if link_type == "URL":
				shortcuts.append({"label": label, "url": link_to, "type": "URL"})
			else:
				shortcuts.append({"label": label, "link_to": link_to, "type": link_type, "doc_view": ""})
		idx += 1
		content.append({"id": f"spacer-{idx}", "type": "spacer", "data": {"col": 12}})
	return content, shortcuts


def _make_workspace(name, module, sections, parent_page, sequence_id):
	content, shortcuts = _build_content_and_shortcuts(sections)
	doc = frappe.new_doc("Workspace")
	doc.name = name
	doc.label = name
	doc.title = name
	doc.module = module
	doc.public = 1
	doc.is_hidden = 0
	doc.icon = "list"
	doc.indicator_color = "blue"
	doc.parent_page = parent_page or ""
	doc.sequence_id = sequence_id
	doc.content = json.dumps(content)
	for sc in shortcuts:
		doc.append("shortcuts", sc)
	doc.insert(ignore_permissions=True)


def create_workspace():
	# Rebuilt on every install/migrate so the workspace tree always matches
	# the app's current module structure. Deleting the parent alone doesn't
	# cascade to children in Frappe, so every workspace this app owns
	# (parent + all children) is dropped and recreated together each time.
	all_names = [TOP_WORKSPACE] + [name for name, _module, _sections in CHILD_WORKSPACES]
	for name in all_names:
		if frappe.db.exists("Workspace", name):
			frappe.delete_doc("Workspace", name, force=True, ignore_permissions=True)

	# The parent's own content is a set of tiles linking to every child
	# workspace -- otherwise landing on "CA Firm" itself shows nothing,
	# since all the real shortcuts live on the children.
	module_tiles = [
		(name, f"/app/{_workspace_route(name)}", "URL")
		for name, _module, _sections in CHILD_WORKSPACES
	]
	_make_workspace(
		TOP_WORKSPACE, "CA Firm Setup",
		[("Modules", module_tiles)],
		parent_page=None, sequence_id=1.0,
	)

	for i, (name, module, sections) in enumerate(CHILD_WORKSPACES, start=1):
		_make_workspace(name, module, sections, parent_page=TOP_WORKSPACE, sequence_id=float(i))

	# Best-effort cache/sidebar-pin cleanup -- must never be allowed to raise
	# past this point, since the caller commits per-step and a failure here
	# would roll back the workspace inserts above along with it.
	try:
		for name in all_names:
			frappe.delete_doc_if_exists("Workspace Sidebar", name, force=True)
		frappe.clear_cache()
	except Exception:
		frappe.log_error(title="CA Firm: workspace cache/sidebar cleanup failed (workspaces themselves were created)")
