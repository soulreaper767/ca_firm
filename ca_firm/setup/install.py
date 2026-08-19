import frappe


def after_install():
	_run_setup()


def after_migrate():
	_run_setup()


def _run_setup():
	from ca_firm.setup import (
		custom_fields, dashboard, kanban, masters, native_permissions, roles, workflow, workspace,
	)

	# Each step commits on success and rolls back + logs on failure, so one
	# broken step (e.g. an API signature that changes between Frappe
	# versions) can never silently undo everything else that already
	# succeeded in this migrate/install run -- which is exactly what
	# happened when an exception in the workspace step rolled back the
	# whole after_migrate transaction, including the workspace insert that
	# had *just* succeeded moments earlier in the same transaction.
	steps = [
		("roles", roles.create_roles),
		("custom_fields", custom_fields.create_all),
		("native_permissions", native_permissions.create_all),
		("masters", masters.create_all),
		("workspace", workspace.create_workspace),
		("dashboard", dashboard.create_all),
		("kanban", kanban.create_kanban_boards),
		("workflow", workflow.create_all),
	]
	for label, step in steps:
		try:
			step()
			frappe.db.commit()  # nosemgrep
		except Exception:
			frappe.db.rollback()
			frappe.log_error(title=f"CA Firm: setup step '{label}' failed")
