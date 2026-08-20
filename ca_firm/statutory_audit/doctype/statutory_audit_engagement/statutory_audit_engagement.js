frappe.ui.form.on("Statutory Audit Engagement", {
	refresh(frm) {
		if (!frm.doc.__islocal && ["Completed", "Archived"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Roll Forward to Next Year"), () => {
				const dialog = new frappe.ui.Dialog({
					title: __("Roll Forward Engagement"),
					fields: [
						{
							fieldname: "client_engagement", fieldtype: "Link", options: "Client Engagement",
							label: __("Client Engagement (new/renewed agreement)"), reqd: 1,
							get_query: () => ({ filters: { client: frm.doc.client } }),
						},
						{ fieldname: "financial_year", fieldtype: "Data", label: __("Financial Year"), reqd: 1 },
						{ fieldname: "cb1", fieldtype: "Column Break" },
						{ fieldname: "period_start", fieldtype: "Date", label: __("Period Start") },
						{ fieldname: "period_end", fieldtype: "Date", label: __("Period End") },
					],
					primary_action_label: __("Create"),
					primary_action: (values) => {
						frm.call("roll_forward", values).then((r) => {
							dialog.hide();
							if (r.message) {
								frappe.set_route("Form", "Statutory Audit Engagement", r.message);
							}
						});
					},
				});
				dialog.show();
			});
		}
	},
});
