import frappe

ROLES = [
	"CA Firm Partner",
	"CA Firm Manager",
	"CA Firm Job Incharge",
	"CA Firm Supervisor",
	"CA Firm Senior",
	"CA Firm Semi Senior",
	"CA Firm Article Assistant",
	"CA Firm EQCR Partner",
	"CA Firm Admin",
	"CA Firm Client",
]

# All roles get Desk access: internal team roles use the full workspace;
# the Client role also gets Desk access (but only Read/limited-Write permission
# on a handful of doctypes - see the `permissions` block on each DocType), so
# that logging into /app shows them a workspace automatically filtered down
# to just what they're permitted to see (Checklist Instance / Audit Query /
# Deliverable), acting as a lightweight client portal without custom web pages.
DESK_ACCESS_ROLES = set(ROLES)


def create_roles():
	for role_name in ROLES:
		if frappe.db.exists("Role", role_name):
			continue
		role = frappe.new_doc("Role")
		role.role_name = role_name
		role.desk_access = 1 if role_name in DESK_ACCESS_ROLES else 0
		role.insert(ignore_permissions=True)
