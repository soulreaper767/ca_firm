frappe.ui.form.on("Internal Audit Observation", {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Escalate to Audit"), () => {
				frm.call("escalate_to_audit");
			}, __("Statutory Audit"));
		}
	},
});
