frappe.ui.form.on("Client Chart of Accounts Mapping", {
	refresh(frm) {
		frm.set_query("parent_account", () => ({
			filters: { client: frm.doc.client, is_group: 1, name: ["!=", frm.doc.name] },
		}));
	},
	client(frm) {
		frm.set_value("parent_account", "");
	},
});
