frappe.ui.form.on("Checklist Instance", {
	refresh(frm) {
		if (frm.doc.template && !frm.doc.__islocal) {
			frm.add_custom_button(__("Re-apply Template Rules"), () => {
				frm.call("populate_from_template").then(() => {
					frm.refresh();
					frappe.show_alert({ message: __("Items refreshed from template"), indicator: "green" });
				});
			});
		}
	},
});
