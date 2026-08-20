import frappe


def after_install():
	_run_setup()


def after_migrate():
	_run_setup()


def _run_setup():
	from ca_firm.setup import (
		custom_fields, dashboard, kanban, masters, native_permissions, print_formats, roles, unblock_modules,
		workflow, workspace,
	)

	# Each step commits on success and rolls back + logs on failure, so one
	# broken step can never silently undo everything else that already
	# succeeded in this migrate/install run.
	steps = [
		("roles", roles.create_roles),
		("custom_fields", custom_fields.create_all),
		("native_permissions", native_permissions.create_all),
		("unblock_modules", unblock_modules.create_all),
		("masters", masters.create_all),
		("workspace", workspace.create_workspace),
		("dashboard", dashboard.create_all),
		("kanban", kanban.create_kanban_boards),
		("print_formats", print_formats.create_all),
		("workflow", workflow.create_all),
	]
	for label, step in steps:
		try:
			step()
			frappe.db.commit()  # nosemgrep
		except Exception:
			frappe.db.rollback()
			frappe.log_error(title=f"CA Firm: setup step '{label}' failed")
