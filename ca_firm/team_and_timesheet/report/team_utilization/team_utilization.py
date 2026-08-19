import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Staff Member", "width": 150},
		{"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 130},
		{"label": "Total Hours", "fieldname": "total_hours", "fieldtype": "Float", "width": 110},
		{"label": "Billable Hours", "fieldname": "billable_hours", "fieldtype": "Float", "width": 120},
		{"label": "Billable %", "fieldname": "billable_percent", "fieldtype": "Percent", "width": 100},
		{"label": "Engagements Worked On", "fieldname": "engagement_count", "fieldtype": "Int", "width": 170},
	]


def get_data(filters):
	conditions = ["ts.status = 'Approved'"]
	values = {}
	if filters.get("from_date"):
		conditions.append("ts.timesheet_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("ts.timesheet_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]
	if filters.get("staff_member"):
		conditions.append("ts.staff_member = %(staff_member)s")
		values["staff_member"] = filters["staff_member"]

	where_clause = " and ".join(conditions)
	rows = frappe.db.sql(
		f"""
		select
			ts.staff_member as staff_member,
			sm.designation as designation,
			sum(te.hours) as total_hours,
			sum(case when te.is_billable = 1 then te.hours else 0 end) as billable_hours,
			count(distinct te.engagement) as engagement_count
		from `tabTimesheet Entry` te
		inner join `tabTimesheet` ts on ts.name = te.parent
		left join `tabStaff Member` sm on sm.name = ts.staff_member
		where {where_clause}
		group by ts.staff_member
		order by total_hours desc
		""",
		values,
		as_dict=1,
	)
	for row in rows:
		row["billable_percent"] = (row.billable_hours / row.total_hours * 100) if row.total_hours else 0
	return rows
