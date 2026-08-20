import frappe

# Defaults to "engagements I hold a leadership role on" for the viewing
# user (Engagement Partner / Manager / Job Incharge), so a Partner opening
# this report sees their own book without filtering anything -- tick
# "Show All" to see the whole firm's engagements instead (still governed by
# normal Statutory Audit Engagement read permissions).


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Financial Year", "fieldname": "financial_year", "fieldtype": "Data", "width": 110},
		{"label": "My Role", "fieldname": "my_role", "fieldtype": "Data", "width": 130},
		{"label": "Partner", "fieldname": "engagement_partner", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Manager", "fieldname": "engagement_manager", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Job Incharge", "fieldname": "job_incharge", "fieldtype": "Link", "options": "Employee", "width": 140},
		{"label": "Team Size", "fieldname": "team_size", "fieldtype": "Int", "width": 90},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Target Completion", "fieldname": "target_completion_date", "fieldtype": "Date", "width": 120},
		{"label": "Days Remaining", "fieldname": "days_remaining", "fieldtype": "Int", "width": 110},
	]


def get_data(filters):
	my_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	conditions = {}
	for field in ("client", "status", "financial_year"):
		if filters.get(field):
			conditions[field] = filters[field]

	if not filters.get("show_all") and my_employee:
		# frappe.get_all's filters/or_filters combine as (filters) OR
		# (or_filters) at the top level, not AND -- so mixing them here
		# would silently ignore the client/status/financial_year filters
		# whenever they didn't also match a role. Resolve the "my role"
		# membership as its own query first, then AND it in via a plain
		# "name in [...]" filter alongside everything else.
		my_engagement_names = frappe.get_all(
			"Statutory Audit Engagement",
			or_filters={
				"engagement_partner": my_employee,
				"engagement_manager": my_employee,
				"job_incharge": my_employee,
			},
			pluck="name",
		)
		if not my_engagement_names:
			return []
		conditions["name"] = ["in", my_engagement_names]

	records = frappe.get_all(
		"Statutory Audit Engagement", filters=conditions,
		fields=["name", "client", "financial_year", "engagement_partner", "engagement_manager",
		        "job_incharge", "status", "target_completion_date"],
		order_by="modified desc",
	)

	if not records:
		return records

	names = [r.name for r in records]
	team_counts = {}
	for row in frappe.get_all(
		"Statutory Audit Team Member", filters={"parent": ["in", names]}, fields=["parent"]
	):
		team_counts[row.parent] = team_counts.get(row.parent, 0) + 1

	today = frappe.utils.getdate()
	for r in records:
		r["team_size"] = team_counts.get(r.name, 0)
		r["days_remaining"] = (r.target_completion_date - today).days if r.target_completion_date else None
		roles = []
		if my_employee and r.engagement_partner == my_employee:
			roles.append("Partner")
		if my_employee and r.engagement_manager == my_employee:
			roles.append("Manager")
		if my_employee and r.job_incharge == my_employee:
			roles.append("Job Incharge")
		r["my_role"] = ", ".join(roles)
	return records
