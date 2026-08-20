import frappe

# Aggregate workload per staff member across active engagements -- informs
# who a Partner/Manager should assign to a new engagement or FS area.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Employee", "width": 160},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 140},
		{"label": "Active Engagements", "fieldname": "active_engagements", "fieldtype": "Int", "width": 130},
		{"label": "Total Allocated Hours", "fieldname": "total_allocated_hours", "fieldtype": "Float", "width": 150},
	]


def get_data(filters):
	active_names = frappe.get_all(
		"Statutory Audit Engagement",
		filters={"status": ["not in", ["Completed", "Archived"]]},
		pluck="name",
	)
	if not active_names:
		return []

	team_rows = frappe.get_all(
		"Statutory Audit Team Member",
		filters={"parent": ["in", active_names]},
		fields=["staff_member", "allocated_hours_budget"],
	)
	if not team_rows:
		return []

	by_staff = {}
	for row in team_rows:
		if not row.staff_member:
			continue
		agg = by_staff.setdefault(row.staff_member, {"count": 0, "hours": 0.0})
		agg["count"] += 1
		agg["hours"] += frappe.utils.flt(row.allocated_hours_budget)

	if filters.get("staff_member"):
		by_staff = {k: v for k, v in by_staff.items() if k == filters["staff_member"]}

	designations = {
		e.name: e.designation
		for e in frappe.get_all("Employee", filters={"name": ["in", list(by_staff.keys())]}, fields=["name", "designation"])
	}

	data = [
		{
			"staff_member": staff,
			"designation": designations.get(staff),
			"active_engagements": agg["count"],
			"total_allocated_hours": agg["hours"],
		}
		for staff, agg in by_staff.items()
	]
	data.sort(key=lambda r: -r["active_engagements"])
	return data
