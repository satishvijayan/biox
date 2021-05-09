frappe.provide('frappe.dashboards.chart_sources');
// frappe.provide('frappe.query_report')
var d = new Date();
var m = 3
var d1 = new Date(d.getFullYear(),d.getMonth()-m,1);

frappe.dashboards.chart_sources["Simple Dashboard 1"] = {

	method: "biox.biox.dashboard_chart_source.simple_dashboard_1.simple_dashboard_1.get",
	filters: [
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": d1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.add_months(d1,m),-1)
		},
		{
			"fieldname":"show_drafts",
			"label": __("Include Draft Documents?"),
			"fieldtype": "Check"
		},

	]
}