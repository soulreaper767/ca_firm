frappe.ui.form.on("Inventory Count Sheet", {
	refresh(frm) {
		if (!frm.doc.__islocal && frm.doc.total_variance_value) {
			frm.add_custom_button(__("Flag Variance to Audit"), () => {
				frm.call("flag_variance_to_audit");
			}, __("Statutory Audit"));
		}
	},
});
