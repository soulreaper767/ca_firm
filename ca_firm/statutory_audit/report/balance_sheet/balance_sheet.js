frappe.query_reports["Balance Sheet"] = {
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
