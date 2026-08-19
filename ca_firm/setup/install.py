import frappe


def after_install():
	_run_setup()
	frappe.db.commit()  # nosemgrep


def after_migrate():
	_run_setup()


def _run_setup():
	from ca_firm.setup import custom_fields, dashboard, kanban, masters, roles, workspace

	roles.create_roles()
	custom_fields.create_all()
	masters.create_all()
	workspace.create_workspace()
	dashboard.create_all()
	kanban.create_kanban_boards()
