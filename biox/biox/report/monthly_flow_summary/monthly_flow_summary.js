// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
// https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/
// Sample report
// # Satish Vijayan 6/3/21



var d = new Date();
var d1 = new Date(d.getFullYear(),d.getMonth()-12,1);

frappe.query_reports["Monthly Flow Summary"] = {
	"filters": [	
		
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": d1,
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.add_months(d1,13),-1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"customer",
			"label": __("Customer (Optional)"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"show_drafts",
			"label": __("Include Draft Documents?"),
			"fieldtype": "Check",
			"width": "60px"
		}
	]
}



// frappe.datetime.add_days(date, days);   // add n days to a date
// frappe.datetime.add_months(date, months); // add n months to a date
// frappe.datetime.month_end(date);  // returns the first day from the month of the given date
// frappe.datetime.month_start(date); // returns the last day from the month of the given date
// frappe.datetime.get_day_diff(begin, end); // returns the days between 2 dates
// https://discuss.erpnext.com/t/how-to-get-today-date/4554/17

// ModuleNotFoundError: No module named 'erpnext.projects.report.monthly_measurement_report.monthly_measurement_report'