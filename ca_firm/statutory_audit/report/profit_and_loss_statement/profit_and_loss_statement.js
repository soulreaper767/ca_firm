frappe.query_reports["Profit and Loss Statement"] = {
	filters: [
		{
			fieldname: "engagement",
			label: __("Engagement"),
			fieldtype: "Link",
			options: "Statutory Audit Engagement",
			reqd: 1,
		},
	],
};
