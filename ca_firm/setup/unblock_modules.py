import frappe

# If any user (most plausibly Administrator, from earlier ERPNext/HRMS setup
# or a stray toggle) has one of our modules in their per-user "Block
# Modules" list, our workspaces are silently excluded from their sidebar --
# Workspace.get_workspaces() filters by `module not in blocked_modules` for
# the *viewing* user, which a plain `frappe.get_all` query never surfaces.
# This is defensive: it costs nothing to run even if it was never the
# actual cause.
OUR_MODULES = [
	"CA Firm Setup", "Client Management", "Engagement Management", "Statutory Audit",
	"Tax", "Internal Audit", "Review Engagements", "Certification Engagements",
	"Inventory Audit", "Advisory", "Company Secretarial", "Bookkeeping and Accounting",
]


def create_all():
	try:
		frappe.db.delete("Block Module", {"module": ["in", OUR_MODULES]})
	except Exception:
		frappe.log_error(title="CA Firm: failed to clear blocked modules")
