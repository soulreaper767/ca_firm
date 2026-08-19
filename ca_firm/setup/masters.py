import frappe

from ca_firm.setup import seed_data as seed


def create_designations():
	for d in seed.DESIGNATIONS:
		if frappe.db.exists("Designation", d["designation_name"]):
			continue
		doc = frappe.new_doc("Designation")
		doc.update(d)
		doc.insert(ignore_permissions=True)


def create_audit_standards():
	for code, title, category in seed.AUDIT_STANDARDS:
		if frappe.db.exists("Audit Standard", code):
			continue
		frappe.get_doc({
			"doctype": "Audit Standard",
			"standard_code": code,
			"title": title,
			"category": category,
		}).insert(ignore_permissions=True)


def create_fs_areas():
	for name, head, risk in seed.FS_AREAS:
		if frappe.db.exists("Financial Statement Area", name):
			continue
		frappe.get_doc({
			"doctype": "Financial Statement Area",
			"area_name": name,
			"fs_head": head,
			"typical_risk_level": risk,
		}).insert(ignore_permissions=True)


def create_assertions():
	for name, category in seed.ASSERTIONS:
		if frappe.db.exists("Assertion", name):
			continue
		frappe.get_doc({
			"doctype": "Assertion", "assertion_name": name, "category": category,
		}).insert(ignore_permissions=True)


def create_risk_categories():
	for name, risk_type in seed.RISK_CATEGORIES:
		if frappe.db.exists("Risk Category", name):
			continue
		frappe.get_doc({
			"doctype": "Risk Category", "risk_category_name": name, "risk_type": risk_type,
		}).insert(ignore_permissions=True)


def create_applicable_laws():
	for name in seed.APPLICABLE_LAWS:
		if frappe.db.exists("Applicable Law", name):
			continue
		frappe.get_doc({"doctype": "Applicable Law", "law_name": name}).insert(ignore_permissions=True)


def create_procedure_types():
	for name in seed.PROCEDURE_TYPES:
		if frappe.db.exists("Audit Procedure Type", name):
			continue
		frappe.get_doc({
			"doctype": "Audit Procedure Type", "procedure_type_name": name,
		}).insert(ignore_permissions=True)


def create_caat_templates():
	for name, category, fs_area in seed.CAAT_TEMPLATES:
		if frappe.db.exists("CAAT Test Template", name):
			continue
		doc = frappe.new_doc("CAAT Test Template")
		doc.test_name = name
		doc.test_category = category
		if fs_area:
			doc.applicable_fs_area = fs_area
		doc.insert(ignore_permissions=True)


def create_checklist_templates():
	for tmpl in seed.CHECKLIST_TEMPLATES:
		if frappe.db.exists("Checklist Template", tmpl["template_name"]):
			continue
		doc = frappe.new_doc("Checklist Template")
		doc.template_name = tmpl["template_name"]
		doc.category = tmpl["category"]
		for i, particular in enumerate(tmpl["items"], start=1):
			doc.append("items", {"item_no": i, "particular": particular, "is_mandatory": 1})
		doc.insert(ignore_permissions=True)


def create_audit_program_templates():
	for tmpl in seed.AUDIT_PROGRAM_TEMPLATES:
		if frappe.db.exists("Audit Program Template", tmpl["template_name"]):
			continue
		doc = frappe.new_doc("Audit Program Template")
		doc.template_name = tmpl["template_name"]
		doc.fs_area = tmpl["fs_area"]
		for i, (desc, assertion, ptype, is_caat) in enumerate(tmpl["steps"], start=1):
			doc.append("steps", {
				"step_no": i,
				"procedure_description": desc,
				"assertion": assertion,
				"procedure_type": ptype,
				"is_caat": is_caat,
			})
		doc.insert(ignore_permissions=True)


def create_all():
	steps = [
		create_designations,
		create_audit_standards,
		create_fs_areas,
		create_assertions,
		create_risk_categories,
		create_applicable_laws,
		create_procedure_types,
		create_caat_templates,
		create_checklist_templates,
		create_audit_program_templates,
	]
	for step in steps:
		try:
			step()
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to seed master data via {step.__name__}")
