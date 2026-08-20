frappe.ui.form.on("Bookkeeping Task", {
	refresh(frm) {
		if (!frm.doc.__islocal && frm.doc.linked_head) {
			frm.add_custom_button(__("Escalate to Audit"), () => {
				frm.call("escalate_to_audit");
			}, __("Statutory Audit"));
		}
	},
});
