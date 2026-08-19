import frappe
from frappe.utils.nestedset import NestedSet


class ClientGroup(NestedSet):
	nsm_parent_field = "parent_client_group"
