import frappe

BOARDS = [
	("Engagement", "Engagement Pipeline", "status"),
	("Audit Procedure", "Audit Procedure Board", "status"),
	("Review Note", "Review Notes Board", "status"),
	("Audit Finding", "Audit Findings Board", "status"),
	("QCR Finding", "QCR Findings Board", "status"),
]


def create_kanban_boards():
	from frappe.desk.doctype.kanban_board.kanban_board import quick_kanban_board

	for doctype, board_name, field_name in BOARDS:
		if frappe.db.exists("Kanban Board", board_name):
			continue
		try:
			quick_kanban_board(doctype, board_name, field_name)
		except Exception:
			frappe.log_error(title=f"CA Firm: failed to create kanban board {board_name}")
