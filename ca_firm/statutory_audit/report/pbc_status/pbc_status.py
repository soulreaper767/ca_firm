import frappe


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": "Engagement", "fieldname": "engagement", "fieldtype": "Link", "options": "Statutory Audit Engagement", "width": 140},
		{"label": "Client", "fieldname": "client", "fieldtype": "Link", "options": "Customer", "width": 170},
		{"label": "Item", "fieldname": "particular", "fieldtype": "Data", "width": 260},
		{"label": "Due Date", "fieldname": "due_date", "fieldtype": "Date", "width": 100},
		{"label": "Received Date", "fieldname": "received_date", "fieldtype": "Date", "width": 110},
		{"label": "Status", "fieldname": "pbc_status", "fieldtype": "Data", "width": 100},
	]


def get_data(filters):
	pbc_instances = frappe.get_all(
		"Checklist Instance",
		filters={"template": ["in", frappe.get_all(
			"Checklist Template", filters={"category": "PBC - Documents Required"}, pluck="name"
		)]},
		fields=["name", "engagement"],
	)
	if filters.get("engagement"):
		pbc_instances = [i for i in pbc_instances if i.engagement == filters["engagement"]]
	if not pbc_instances:
		return []

	inst_names = [i.name for i in pbc_instances]
	eng_map = {i.name: i.engagement for i in pbc_instances}
	eng_names = list({e for e in eng_map.values() if e})
	client_map = {
		e.name: e.client
		for e in frappe.get_all("Statutory Audit Engagement", filters={"name": ["in", eng_names]}, fields=["name", "client"])
	}

	items = frappe.get_all(
		"Checklist Instance Item",
		filters={"parent": ["in", inst_names], "is_applicable": 1},
		fields=["parent", "particular", "due_date", "received_date", "is_complete"],
	)

	today = frappe.utils.getdate()
	rows = []
	for item in items:
		if filters.get("outstanding_only") and item.is_complete:
			continue
		if item.received_date:
			status = "Received"
		elif item.due_date and item.due_date < today:
			status = "Overdue"
		else:
			status = "Outstanding"
		engagement = eng_map.get(item.parent)
		rows.append({
			"engagement": engagement,
			"client": client_map.get(engagement),
			"particular": item.particular,
			"due_date": item.due_date,
			"received_date": item.received_date,
			"pbc_status": status,
		})
	rows.sort(key=lambda r: (r["due_date"] or frappe.utils.getdate("2100-01-01")))
	return rows
