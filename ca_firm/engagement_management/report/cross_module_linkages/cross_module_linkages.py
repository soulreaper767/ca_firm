import frappe

# The single firm-wide view of every cross-module linkage raised by any
# assignment module -- e.g. a Tax adjustment that also needs an Audit
# Adjustment, or an Internal Audit observation flagged against a
# Statutory Audit working paper. Filter by client or financial head to see
# every module touching the same figure.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Relationship", "fieldname": "relationship_type", "fieldtype": "Link", "options": "Cross Reference Type", "width": 160},
		{"label": "Source Doctype", "fieldname": "source_doctype", "fieldtype": "Data", "width": 150},
		{"label": "Source Record", "fieldname": "source_name", "fieldtype": "Dynamic Link", "options": "source_doctype", "width": 150},
		{"label": "Target Doctype", "fieldname": "target_doctype", "fieldtype": "Data", "width": 150},
		{"label": "Target Record", "fieldname": "target_name", "fieldtype": "Dynamic Link", "options": "target_doctype", "width": 150},
		{"label": "Linked Head", "fieldname": "linked_head", "fieldtype": "Link", "options": "Chart of Accounts Head", "width": 150},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Raised By", "fieldname": "raised_by", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Raised On", "fieldname": "creation", "fieldtype": "Datetime", "width": 150},
	]


def get_data(filters):
	conditions = {}
	for field in ("client", "relationship_type", "status", "linked_head"):
		if filters.get(field):
			conditions[field] = filters[field]

	return frappe.get_all(
		"Engagement Cross Reference",
		filters=conditions,
		fields=["client", "relationship_type", "source_doctype", "source_name",
		        "target_doctype", "target_name", "linked_head", "status", "raised_by", "creation"],
		order_by="creation desc",
	)
