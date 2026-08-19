import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Staff Member", "fieldname": "staff_member", "fieldtype": "Link", "options": "Staff Member", "width": 150},
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Engagement", "width": 150},
		{"label": "FS Area", "fieldname": "fs_area", "fieldtype": "Link", "options": "Financial Statement Area", "width": 160},
		{"label": "Billable Hours", "fieldname": "billable_hours", "fieldtype": "Float", "width": 120},
		{"label": "Non-Billable Hours", "fieldname": "non_billable_hours", "fieldtype": "Float", "width": 140},
		{"label": "Total Hours", "fieldname": "total_hours", "fieldtype": "Float", "width": 110},
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
	if filters.get("engagement"):
		conditions.append("te.engagement = %(engagement)s")
		values["engagement"] = filters["engagement"]

	where_clause = " and ".join(conditions)
	return frappe.db.sql(
		f"""
		select
			ts.staff_member as staff_member,
			te.engagement as engagement,
			te.fs_area as fs_area,
			sum(case when te.is_billable = 1 then te.hours else 0 end) as billable_hours,
			sum(case when te.is_billable = 0 then te.hours else 0 end) as non_billable_hours,
			sum(te.hours) as total_hours
		from `tabTimesheet Entry` te
		inner join `tabTimesheet` ts on ts.name = te.parent
		where {where_clause}
		group by ts.staff_member, te.engagement, te.fs_area
		order by ts.staff_member, total_hours desc
		""",
		values,
		as_dict=1,
	)
