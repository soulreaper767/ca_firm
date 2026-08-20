frappe.ui.form.on("Certification Procedure", {
	refresh(frm) {
		frm.set_query("linked_account", () => ({
			filters: { client: frm.doc.client, is_group: 0 },
		}));
	},
});
