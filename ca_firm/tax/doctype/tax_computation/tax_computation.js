frappe.ui.form.on("Tax Computation", {
	refresh(frm) {
		if (frm.doc.source_statutory_engagement && !frm.doc.__islocal) {
			frm.add_custom_button(__("Pull Accounting Profit from Audit"), () => {
				frm.call("pull_accounting_profit_from_audit").then(() => frm.reload_doc());
			}, __("Statutory Audit"));

			frm.add_custom_button(__("Pull Full P&L Breakdown"), () => {
				frm.call("pull_full_pl_breakdown").then(() => frm.reload_doc());
			}, __("Statutory Audit"));

			frm.add_custom_button(__("Flag Items to Audit"), () => {
				frm.call("flag_items_to_audit");
			}, __("Statutory Audit"));
		}

		if (frm.doc.adjustment_items && frm.doc.adjustment_items.length && !frm.doc.__islocal) {
			frm.add_custom_button(__("Compute Taxable Income from Items"), () => {
				frm.call("compute_from_adjustment_items").then(() => frm.reload_doc());
			});
		}
	},
});
