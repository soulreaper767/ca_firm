frappe.ui.form.on("Review Procedure", {
	refresh(frm) {
		frm.set_query("linked_account", () => ({
			filters: { client: frm.doc.client, is_group: 0 },
		}));

		if (!frm.doc.__islocal && frm.doc.conclusion === "Matter Noted") {
			frm.add_custom_button(__("Escalate to Audit"), () => {
				frm.call("escalate_to_audit");
			}, __("Statutory Audit"));
		}
	},
});
