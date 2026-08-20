frappe.ui.form.on("Statement of Changes in Equity", {
	refresh(frm) {
		if (frm.doc.engagement && !frm.doc.__islocal) {
			frm.add_custom_button(__("Pull Opening/Closing Balances"), () => {
				frm.call("pull_opening_closing_balances").then(() => frm.reload_doc());
			});
		}
	},
});
