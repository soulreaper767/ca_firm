import frappe


def get_line_item_amounts(engagement):
	"""Aggregate a Statutory Audit Engagement's Trial Balance into natural
	(always-positive-on-its-own-side) amounts per FS Line Item, current and
	prior year. Shared by the Balance Sheet and Profit and Loss Statement
	reports so both walk the exact same figures off the exact same Trial
	Balance -- the two statements are never allowed to drift apart."""
	tb_name = frappe.db.get_value("Trial Balance", {"engagement": engagement}, "name")
	if not tb_name:
		return {}

	entries = frappe.get_all(
		"Trial Balance Entry",
		filters={"parent": tb_name},
		fields=["mapped_head", "current_year_debit", "current_year_credit",
		        "prior_year_debit", "prior_year_credit"],
	)
	if not entries:
		return {}

	heads = frappe.get_all(
		"Chart of Accounts Head",
		filters={"name": ["in", list({e.mapped_head for e in entries if e.mapped_head})]},
		fields=["name", "fs_line_item", "nature"],
	)
	head_by_name = {h.name: h for h in heads}

	amounts = {}
	for e in entries:
		head = head_by_name.get(e.mapped_head)
		if not head or not head.fs_line_item:
			continue
		sign = 1 if head.nature == "Debit" else -1
		cur = sign * (frappe.utils.flt(e.current_year_debit) - frappe.utils.flt(e.current_year_credit))
		prior = sign * (frappe.utils.flt(e.prior_year_debit) - frappe.utils.flt(e.prior_year_credit))
		existing_cur, existing_prior = amounts.get(head.fs_line_item, (0.0, 0.0))
		amounts[head.fs_line_item] = (existing_cur + cur, existing_prior + prior)

	return amounts


def build_statement_rows(statement_type, amounts_by_line):
	"""Walk FS Line Item's parent_line_item hierarchy for the given
	statement type (Balance Sheet / Profit and Loss / Cash Flow Statement /
	Statement of Changes in Equity), computing each subtotal as the sum of
	its own directly-mapped heads plus every descendant, ordered by
	sequence, indented by depth."""
	line_items = frappe.get_all(
		"FS Line Item", filters={"statement_type": statement_type},
		fields=["name", "line_item_name", "classification", "parent_line_item", "sequence", "is_subtotal"],
	)
	by_parent = {}
	by_name = {}
	for li in line_items:
		by_parent.setdefault(li.parent_line_item, []).append(li)
		by_name[li.name] = li
	for children in by_parent.values():
		children.sort(key=lambda x: x.sequence or 0)

	rows = []

	def walk(line_item, depth):
		own_cur, own_prior = amounts_by_line.get(line_item.name, (0.0, 0.0))
		children = by_parent.get(line_item.name, [])
		cur, prior = own_cur, own_prior
		for child in children:
			c_cur, c_prior = walk(child, depth + 1)
			cur += c_cur
			prior += c_prior
		rows.append({
			"line_item": ("    " * depth) + line_item.line_item_name,
			"current_year": cur,
			"prior_year": prior,
			"is_subtotal": line_item.is_subtotal,
			"classification": line_item.classification,
		})
		return cur, prior

	for root in by_parent.get(None, []) + by_parent.get("", []):
		walk(root, 0)

	return rows
