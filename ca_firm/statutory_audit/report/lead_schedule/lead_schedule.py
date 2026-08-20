import frappe

# The classic audit "lead schedule": groups a client's raw trial balance
# accounts (via their standing Chart of Accounts Mapping) up into the
# standard FS Line Items, comparing current year to prior year -- the
# entry point every fieldwork area (Revenue, PPE, Receivables, etc.)
# starts from.


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	if not filters.get("engagement"):
		frappe.msgprint("Select an Engagement to view its lead schedule.")
		return columns, []
	data = get_data(filters["engagement"])
	return columns, data


def get_columns():
	return [
		{"label": "FS Line Item", "fieldname": "fs_line_item", "fieldtype": "Link", "options": "FS Line Item", "width": 220},
		{"label": "Head", "fieldname": "head_name", "fieldtype": "Link", "options": "Chart of Accounts Head", "width": 200},
		{"label": "Current Year", "fieldname": "current_year_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Prior Year", "fieldname": "prior_year_amount", "fieldtype": "Currency", "width": 140},
		{"label": "Variance", "fieldname": "variance", "fieldtype": "Currency", "width": 130},
		{"label": "Variance %", "fieldname": "variance_percent", "fieldtype": "Percent", "width": 100},
	]


def get_data(engagement):
	tb_name = frappe.db.get_value("Trial Balance", {"engagement": engagement}, "name")
	if not tb_name:
		return []

	entries = frappe.get_all(
		"Trial Balance Entry",
		filters={"parent": tb_name},
		fields=["mapped_head", "current_year_debit", "current_year_credit", "prior_year_debit", "prior_year_credit"],
	)
	if not entries:
		return []

	head_names = list({e.mapped_head for e in entries if e.mapped_head})
	heads = {
		h.name: h
		for h in frappe.get_all(
			"Chart of Accounts Head", filters={"name": ["in", head_names]},
			fields=["name", "fs_line_item", "nature"],
		)
	}

	rows_by_head = {}
	for e in entries:
		if not e.mapped_head or e.mapped_head not in heads:
			continue
		head = heads[e.mapped_head]
		sign = 1 if head.nature == "Debit" else -1
		cy = sign * (frappe.utils.flt(e.current_year_debit) - frappe.utils.flt(e.current_year_credit))
		py = sign * (frappe.utils.flt(e.prior_year_debit) - frappe.utils.flt(e.prior_year_credit))
		row = rows_by_head.setdefault(e.mapped_head, {"cy": 0.0, "py": 0.0})
		row["cy"] += cy
		row["py"] += py

	data = []
	for head_name, amounts in rows_by_head.items():
		head = heads[head_name]
		variance = amounts["cy"] - amounts["py"]
		data.append({
			"fs_line_item": head.fs_line_item,
			"head_name": head_name,
			"current_year_amount": amounts["cy"],
			"prior_year_amount": amounts["py"],
			"variance": variance,
			"variance_percent": (variance / amounts["py"] * 100) if amounts["py"] else 0,
		})
	data.sort(key=lambda r: (r["fs_line_item"] or "", r["head_name"] or ""))
	return data
