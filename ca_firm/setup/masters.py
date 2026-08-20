import frappe

from ca_firm.setup import seed_data as seed


def create_simple_masters():
	for master_name, values in seed.SIMPLE_MASTERS.items():
		for title in values:
			if frappe.db.exists(master_name, title):
				continue
			frappe.get_doc({"doctype": master_name, "title": title}).insert(ignore_permissions=True)


def create_designations():
	for d in seed.DESIGNATIONS:
		if frappe.db.exists("Designation", d["designation_name"]):
			continue
		doc = frappe.new_doc("Designation")
		doc.update(d)
		doc.insert(ignore_permissions=True)


def create_all():
	steps = [
		create_simple_masters,
		create_designations,
	]
	for step in steps:
		try:
			step()
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to seed master data via {step.__name__}")
