// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt

frappe.query_reports["Bus Occupancy Rate Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -30),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "route",
			label: __("Route"),
			fieldtype: "Link",
			options: "Bus Route",
		},
		{
			fieldname: "vehicle",
			label: __("Vehicle"),
			fieldtype: "Link",
			options: "Bus Vehicle",
		},
	],
};
