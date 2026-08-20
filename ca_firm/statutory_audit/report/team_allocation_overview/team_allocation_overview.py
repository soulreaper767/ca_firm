import frappe

# "What staff member is engaged with what assignments and what timelines" --
# flattens the team member table across engagements. Defaults to the
# viewing Partner/Manager's own engagements (same rule as My Engagements
# Overview); tick "Show All" for a firm-wide view.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Employee", "width": 150},
		{"label": "Role", "fieldname": "role_in_engagement", "fieldtype": "Data", "width": 120},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Engagement Status", "fieldname": "engagement_status", "fieldtype": "Data", "width": 120},
		{"label": "Allocated Hours", "fieldname": "allocated_hours_budget", "fieldtype": "Float", "width": 110},
		{"label": "Target Completion", "fieldname": "target_completion_date", "fieldtype": "Date", "width": 120},
	]


def get_data(filters):
	my_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	eng_conditions = {}
	for field in ("client", "status"):
		if filters.get(field):
			eng_conditions[field] = filters[field]

	if not filters.get("show_all") and my_employee:
		my_names = frappe.get_all(
			"Statutory Audit Engagement",
			or_filters={"engagement_partner": my_employee, "engagement_manager": my_employee, "job_incharge": my_employee},
			pluck="name",
		)
		if not my_names:
			return []
		eng_conditions["name"] = ["in", my_names]

	engagements = frappe.get_all(
		"Statutory Audit Engagement", filters=eng_conditions,
		fields=["name", "client", "status", "target_completion_date"],
	)
	if not engagements:
		return []
	eng_map = {e.name: e for e in engagements}

	team_filters = {"parent": ["in", list(eng_map.keys())]}
	if filters.get("staff_member"):
		team_filters["staff_member"] = filters["staff_member"]

	team_rows = frappe.get_all(
		"Statutory Audit Team Member", filters=team_filters,
		fields=["parent", "staff_member", "role_in_engagement", "allocated_hours_budget"],
	)

	data = []
	for row in team_rows:
		eng = eng_map.get(row.parent)
		if not eng:
			continue
		data.append({
			"staff_member": row.staff_member,
			"role_in_engagement": row.role_in_engagement,
			"engagement": row.parent,
			"client": eng.client,
			"engagement_status": eng.status,
			"allocated_hours_budget": row.allocated_hours_budget,
			"target_completion_date": eng.target_completion_date,
		})
	data.sort(key=lambda r: (r["staff_member"] or "", r["target_completion_date"] or frappe.utils.getdate("2100-01-01")))
	return data
