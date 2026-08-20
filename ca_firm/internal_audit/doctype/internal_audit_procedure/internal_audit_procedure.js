frappe.ui.form.on("Internal Audit Procedure", {
	refresh(frm) {
		frm.set_query("linked_account", () => ({
			filters: { client: frm.doc.client, is_group: 0 },
		}));
	},
});
