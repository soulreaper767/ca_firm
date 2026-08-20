import frappe

# Only open/in-progress observations, ordered soonest-due-first, so a
# Manager or Partner can see at a glance what remediation is coming due
# across every Internal Audit client -- the follow-up equivalent of the
# Tax module's "Notices Outstanding" report.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Observation", "fieldname": "name", "fieldtype": "Link", "options": "Internal Audit Observation", "width": 130},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Internal Audit Engagement", "width": 130},
		{"label": "Area Reviewed", "fieldname": "area_reviewed", "fieldtype": "Data", "width": 150},
		{"label": "Responsible Person", "fieldname": "responsible_person", "fieldtype": "Data", "width": 140},
		{"label": "Target Date", "fieldname": "target_date", "fieldtype": "Date", "width": 100},
		{"label": "Days Remaining", "fieldname": "days_remaining", "fieldtype": "Int", "width": 110},
		{"label": "Last Follow-Up", "fieldname": "last_follow_up", "fieldtype": "Date", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters):
	conditions = {"status": ["!=", "Closed"]}
	if filters.get("engagement"):
		conditions["engagement"] = filters["engagement"]

	records = frappe.get_all(
		"Internal Audit Observation", filters=conditions,
		fields=["name", "engagement", "area_reviewed", "responsible_person", "target_date", "status"],
		order_by="target_date asc",
	)
	if not records:
		return records

	names = [r.name for r in records]
	follow_ups = frappe.get_all(
		"Internal Audit Follow Up", filters={"parent": ["in", names]},
		fields=["parent", "follow_up_date"], order_by="follow_up_date desc",
	)
	last_follow_up = {}
	for fu in follow_ups:
		if fu.parent not in last_follow_up:
			last_follow_up[fu.parent] = fu.follow_up_date

	today = frappe.utils.getdate()
	for r in records:
		r["last_follow_up"] = last_follow_up.get(r.name)
		r["days_remaining"] = (r.target_date - today).days if r.target_date else None
	return records
