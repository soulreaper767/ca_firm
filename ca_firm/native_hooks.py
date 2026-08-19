"""
Controller logic for DocTypes owned by other apps (ERPNext's Timesheet).
We can't edit erpnext's own controller, so this is wired in via hooks.py
doc_events instead.
"""
import frappe


def timesheet_on_submit(doc, method=None):
	for row in doc.time_logs:
		if not row.audit_procedure:
			continue
		current = frappe.db.get_value("Audit Procedure", row.audit_procedure, "actual_hours") or 0
		frappe.db.set_value(
			"Audit Procedure", row.audit_procedure, "actual_hours",
			frappe.utils.flt(current) + frappe.utils.flt(row.hours),
		)
