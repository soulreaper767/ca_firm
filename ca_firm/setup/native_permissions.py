"""
CA Firm roles need explicit permission on the native ERPNext/HRMS doctypes
we attached custom fields to (Customer, Employee, Company, Designation,
Timesheet) -- those doctypes ship with their own role-based permissions
(Sales User, HR Manager, etc.) that our roles are not part of. Without this,
e.g. a CA Firm Partner cannot open a Customer record at all, and no role can
even select an Employee in a Link field (Link fields require doctype-level
read permission to populate their dropdown).

Uses frappe.permissions.add_permission()/update_permission_property(), the
same API HRMS and other apps use to extend permissions on doctypes they
don't own, writing Custom DocPerm records rather than editing the doctype.
"""
import frappe
from frappe.permissions import add_permission, update_permission_property

R_PARTNER = "CA Firm Partner"
R_MANAGER = "CA Firm Manager"
R_JIC = "CA Firm Job Incharge"
R_SUPERVISOR = "CA Firm Supervisor"
R_SENIOR = "CA Firm Senior"
R_SEMI = "CA Firm Semi Senior"
R_JUNIOR = "CA Firm Article Assistant"
R_EQCR = "CA Firm EQCR Partner"
R_ADMIN = "CA Firm Admin"

ALL_TEAM_ROLES = [R_PARTNER, R_MANAGER, R_JIC, R_SUPERVISOR, R_SENIOR, R_SEMI, R_JUNIOR, R_EQCR, R_ADMIN]

# doctype -> {role: {"read":1, "write":1, "create":1, "delete":1, "permlevel":0}}
GRANTS = {
	"Customer": {
		R_PARTNER: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_ADMIN: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_MANAGER: {"read": 1, "write": 1, "create": 1},
		R_JIC: {"read": 1, "write": 1, "create": 1},
		R_SUPERVISOR: {"read": 1},
		R_SENIOR: {"read": 1},
		R_SEMI: {"read": 1},
		R_JUNIOR: {"read": 1},
	},
	"Company": {
		R_PARTNER: {"read": 1, "write": 1},
		R_ADMIN: {"read": 1, "write": 1},
		R_MANAGER: {"read": 1},
		R_JIC: {"read": 1},
		R_SUPERVISOR: {"read": 1},
		R_SENIOR: {"read": 1},
		R_SEMI: {"read": 1},
		R_JUNIOR: {"read": 1},
	},
	"Designation": {
		R_PARTNER: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_ADMIN: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_MANAGER: {"read": 1, "write": 1, "create": 1},
		R_JIC: {"read": 1},
		R_SUPERVISOR: {"read": 1},
		R_SENIOR: {"read": 1},
		R_SEMI: {"read": 1},
		R_JUNIOR: {"read": 1},
	},
	"Employee": {
		# Base (permlevel 0) read is granted to every team role -- needed
		# just to pick a colleague in a Link field. Sensitive HR sections
		# (bank details, salary, personal/family info) are pushed to
		# permlevel 1 below, which only Partner/Manager/Admin get.
		R_PARTNER: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_ADMIN: {"read": 1, "write": 1, "create": 1, "delete": 1},
		R_MANAGER: {"read": 1, "write": 1, "create": 1},
		R_JIC: {"read": 1},
		R_SUPERVISOR: {"read": 1},
		R_SENIOR: {"read": 1},
		R_SEMI: {"read": 1},
		R_JUNIOR: {"read": 1},
	},
}

# Employee permlevel-1 fields: only Partner/Manager/Admin can see or edit
# compensation and personal HR data; everyone else only ever sees permlevel 0
# (name, designation, department, status, contact details).
EMPLOYEE_PERMLEVEL1_FIELDS = [
	"salary_information", "ctc", "salary_currency", "salary_mode",
	"bank_details_section", "bank_name", "bank_ac_no", "iban",
	"personal_details", "marital_status", "family_background", "blood_group", "health_details",
	"passport_details_section", "passport_number", "valid_upto", "date_of_issue", "place_of_issue",
	"chargeable_rate_per_hour", "cost_rate_per_hour",
]

EMPLOYEE_PERMLEVEL1_ROLES = [R_PARTNER, R_MANAGER, R_ADMIN]


def grant_doctype_permissions():
	for doctype, role_grants in GRANTS.items():
		for role, perms in role_grants.items():
			try:
				add_permission(doctype, role, 0)
				for ptype, value in perms.items():
					update_permission_property(doctype, role, 0, ptype, value)
			except Exception:
				frappe.log_error(title=f"CA Firm: failed to grant {role} on {doctype}")


def set_employee_field_permlevels():
	for fieldname in EMPLOYEE_PERMLEVEL1_FIELDS:
		try:
			frappe.make_property_setter({
				"doctype": "Employee",
				"fieldname": fieldname,
				"property": "permlevel",
				"value": "1",
				"property_type": "Int",
			}, ignore_validate=True)
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to set permlevel on Employee.{fieldname}")

	for role in EMPLOYEE_PERMLEVEL1_ROLES:
		try:
			add_permission("Employee", role, 1)
			update_permission_property("Employee", role, 1, "read", 1)
			update_permission_property("Employee", role, 1, "write", 1)
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to grant permlevel-1 Employee access to {role}")


def create_all():
	grant_doctype_permissions()
	set_employee_field_permlevels()
