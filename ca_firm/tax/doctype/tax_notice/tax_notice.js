frappe.ui.form.on("Tax Notice", {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Escalate to Audit"), () => {
				frm.call("escalate_to_audit");
			}, __("Statutory Audit"));
		}
	},
});
