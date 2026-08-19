import frappe

# Internal firm-management report -- restricted to Partner/Manager both via
# the report's own role list and because it surfaces fee_estimate, which is
# a permlevel-1 field only those roles can read on the Engagement form itself.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "name", "fieldtype": "Link", "options": "Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 160},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
		{"label": "Budgeted Fee", "fieldname": "fee_estimate", "fieldtype": "Currency", "width": 130},
		{"label": "WIP at Cost", "fieldname": "wip_at_cost", "fieldtype": "Currency", "width": 120},
		{"label": "WIP at Chargeable Rate", "fieldname": "wip_at_chargeable", "fieldtype": "Currency", "width": 170},
		{"label": "Realization %", "fieldname": "realization_percent", "fieldtype": "Percent", "width": 120},
		{"label": "Margin over Cost", "fieldname": "margin_over_cost", "fieldtype": "Currency", "width": 140},
	]


def get_data(filters):
	conditions = {}
	for field in ("client", "status"):
		if filters.get(field):
			conditions[field] = filters[field]

	engagements = frappe.get_all(
		"Engagement", filters=conditions, fields=["name", "client", "status", "fee_estimate"]
	)
	if not engagements:
		return []

	names = [e.name for e in engagements]
	wip_rows = frappe.db.sql(
		"""
		select
			td.engagement as engagement,
			sum(td.hours * ifnull(emp.cost_rate_per_hour, 0)) as wip_at_cost,
			sum(td.hours * ifnull(emp.chargeable_rate_per_hour, 0)) as wip_at_chargeable
		from `tabTimesheet Detail` td
		inner join `tabTimesheet` ts on ts.name = td.parent and ts.docstatus = 1
		left join `tabEmployee` emp on emp.name = ts.employee
		where td.engagement in %(names)s
		group by td.engagement
		""",
		{"names": names},
		as_dict=1,
	)
	wip_map = {r.engagement: r for r in wip_rows}

	rows = []
	for e in engagements:
		wip = wip_map.get(e.name, frappe._dict(wip_at_cost=0, wip_at_chargeable=0))
		fee = frappe.utils.flt(e.fee_estimate)
		chargeable = frappe.utils.flt(wip.wip_at_chargeable)
		rows.append({
			"name": e.name,
			"client": e.client,
			"status": e.status,
			"fee_estimate": fee,
			"wip_at_cost": wip.wip_at_cost,
			"wip_at_chargeable": chargeable,
			"realization_percent": (fee / chargeable * 100) if chargeable else 0,
			"margin_over_cost": fee - frappe.utils.flt(wip.wip_at_cost),
		})
	return rows
