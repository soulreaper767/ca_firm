import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Checklist", "fieldname": "name", "fieldtype": "Link", "options": "Checklist Instance", "width": 130},
		{"label": "Template", "fieldname": "checklist_template", "fieldtype": "Link", "options": "Checklist Template", "width": 220},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Client", "width": 150},
		{"label": "Total Items", "fieldname": "total_items", "fieldtype": "Int", "width": 90},
		{"label": "Completed Items", "fieldname": "completed_items", "fieldtype": "Int", "width": 110},
		{"label": "% Complete", "fieldname": "percent_complete", "fieldtype": "Percent", "width": 100},
		{"label": "Overall Status", "fieldname": "overall_status", "fieldtype": "Data", "width": 110},
	]


def get_data(filters):
	conditions = {}
	for field in ("engagement", "client", "checklist_template"):
		if filters.get(field):
			conditions[field] = filters[field]

	instances = frappe.get_all(
		"Checklist Instance",
		filters=conditions,
		fields=["name", "checklist_template", "engagement", "client", "overall_status"],
	)
	rows = []
	for inst in instances:
		items = frappe.get_all(
			"Checklist Instance Item",
			filters={"parent": inst.name},
			fields=["status"],
		)
		total = len(items)
		completed = len([i for i in items if i.status in ("Received", "Not Applicable", "Reviewed")])
		inst["total_items"] = total
		inst["completed_items"] = completed
		inst["percent_complete"] = (completed / total * 100) if total else 0
		rows.append(inst)
	return rows
