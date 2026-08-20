frappe.ui.form.on("Deferred Tax Working", {
	refresh(frm) {
		frm.set_query("linked_account", "items", () => ({
			filters: { client: frm.doc.client, is_group: 0 },
		}));
	},
});
