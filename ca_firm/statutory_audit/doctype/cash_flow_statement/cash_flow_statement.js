frappe.ui.form.on("Cash Flow Statement", {
	refresh(frm) {
		if (frm.doc.engagement && !frm.doc.__islocal) {
			frm.add_custom_button(__("Pull Draft Working Capital Movements"), () => {
				frm.call("pull_draft_operating_activities").then(() => frm.reload_doc());
			}, __("Draft From Trial Balance"));

			frm.add_custom_button(__("Pull Draft Investing Movements"), () => {
				frm.call("pull_draft_investing_activities").then(() => frm.reload_doc());
			}, __("Draft From Trial Balance"));

			frm.add_custom_button(__("Pull Draft Financing Movements"), () => {
				frm.call("pull_draft_financing_activities").then(() => frm.reload_doc());
			}, __("Draft From Trial Balance"));
		}
	},
});
