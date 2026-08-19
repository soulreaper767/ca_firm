import frappe

WORKFLOW_NAME = "Engagement Lifecycle"
DOCUMENT_TYPE = "Engagement"

# (state, style)
STATES = [
	("Draft", ""),
	("Acceptance Pending", "Warning"),
	("Planning", "Warning"),
	("Fieldwork", "Primary"),
	("Manager Review", "Primary"),
	("Partner Review", "Primary"),
	("Completed", "Success"),
	("Archived", "Inverse"),
	("Declined", "Danger"),
]

# (from_state, action, to_state, allowed_role)
TRANSITIONS = [
	("Draft", "Submit for Acceptance", "Acceptance Pending", "CA Firm Job Incharge"),
	("Draft", "Decline", "Declined", "CA Firm Partner"),
	("Acceptance Pending", "Approve Acceptance", "Planning", "CA Firm Partner"),
	("Acceptance Pending", "Decline", "Declined", "CA Firm Partner"),
	("Planning", "Start Fieldwork", "Fieldwork", "CA Firm Job Incharge"),
	("Fieldwork", "Send for Manager Review", "Manager Review", "CA Firm Job Incharge"),
	("Manager Review", "Send Back to Fieldwork", "Fieldwork", "CA Firm Manager"),
	("Manager Review", "Send for Partner Review", "Partner Review", "CA Firm Manager"),
	("Partner Review", "Send Back to Fieldwork", "Fieldwork", "CA Firm Partner"),
	("Partner Review", "Approve and Complete", "Completed", "CA Firm Partner"),
	("Completed", "Archive", "Archived", "CA Firm Partner"),
]


def create_workflow_states():
	for state, style in STATES:
		if frappe.db.exists("Workflow State", state):
			continue
		frappe.get_doc({
			"doctype": "Workflow State", "workflow_state_name": state, "style": style,
		}).insert(ignore_permissions=True)


def create_workflow_actions():
	actions = {action for _, action, _, _ in TRANSITIONS}
	for action in actions:
		if frappe.db.exists("Workflow Action Master", action):
			continue
		frappe.get_doc({
			"doctype": "Workflow Action Master", "workflow_action_name": action,
		}).insert(ignore_permissions=True)


def create_engagement_workflow():
	# Rebuilt on every migrate, same reasoning as the workspace: this is part
	# of the app's structure, not user data, so it should always match source.
	if frappe.db.exists("Workflow", WORKFLOW_NAME):
		frappe.delete_doc("Workflow", WORKFLOW_NAME, force=True, ignore_permissions=True)

	doc = frappe.new_doc("Workflow")
	doc.workflow_name = WORKFLOW_NAME
	doc.document_type = DOCUMENT_TYPE
	doc.is_active = 1
	doc.override_status = 0
	doc.send_email_alert = 0
	doc.workflow_state_field = "status"

	for state, _style in STATES:
		doc.append("states", {
			"state": state,
			"doc_status": "0",
			# allow_edit intentionally left blank: base DocType permissions
			# (see perms_engagement in the doctype JSON) already govern who
			# can edit the record; this workflow only gates who can move it
			# forward via the transition action buttons.
		})

	for from_state, action, to_state, role in TRANSITIONS:
		doc.append("transitions", {
			"state": from_state,
			"action": action,
			"next_state": to_state,
			"allowed": role,
			"allow_self_approval": 1,
		})

	doc.insert(ignore_permissions=True)


def create_all():
	try:
		create_workflow_states()
		create_workflow_actions()
		create_engagement_workflow()
	except Exception:
		frappe.log_error(title="CA Firm: failed to create Engagement workflow")
