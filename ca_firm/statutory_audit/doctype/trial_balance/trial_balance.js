frappe.ui.form.on("Trial Balance", {
	refresh(frm) {
		frm.set_query("client_account", "entries", () => ({
			filters: { client: frm.doc.client, is_group: 0, is_active: 1 },
		}));
	},
});
