frappe.ui.form.on("Audit Report", {
	refresh(frm) {
		if (frm.doc.report_template && !frm.doc.__islocal) {
			frm.add_custom_button(__("Pull from Template"), () => {
				frm.call("pull_from_template").then(() => {
					frm.refresh();
					frappe.show_alert({ message: __("Report content pulled from template"), indicator: "green" });
				});
			});
		}
	},
});
