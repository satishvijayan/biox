// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
// https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/client_statement.js
// Sample report
// # Satish Vijayan 6/3/21
// https://github.com/frappe/datatable/issues/59
// https://maheshlangote.blogspot.com/2018/02/how-to-add-dynamic-columns-in-custom.html
// https://discuss.erpnext.com/t/adding-jquery-datatable-from-external-javascript-and-css-style-with-client-side-custom-script/60467
<<<<<<< HEAD
=======
// https://github.com/frappe/erpnext/blob/5ce0569f80c622d6d7ff480015e8d79b82bf93b5/erpnext/stock/report/batch_wise_balance_history/batch_wise_balance_history.js
>>>>>>> a9aa0967fa8d96e2a5e3ac6e8f2e077dfd0bc4e6
var d = new Date();
var m = 4
var d1 = new Date(d.getFullYear(),d.getMonth()-m,1);


<<<<<<< HEAD
frappe.query_reports["Monthly Measurement Report"] = {
=======
frappe.query_reports["Project Dashboard Report 1"] = {
>>>>>>> a9aa0967fa8d96e2a5e3ac6e8f2e077dfd0bc4e6
	

	"filters": [
		
		{
<<<<<<< HEAD
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
=======
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"get_query": function() {
				let cust = frappe.query_report.get_filter_value('customer');
				return {
					filters: {
						"customer": cust
					}
				};
			}
>>>>>>> a9aa0967fa8d96e2a5e3ac6e8f2e077dfd0bc4e6
		},
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
			"default": frappe.datetime.add_days(frappe.datetime.add_months(d1,m),-1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"show_drafts",
			"label": __("Include Draft Documents?"),
			"fieldtype": "Check",
			"width": "60px"
		},
    	
	]	

  
}



// frappe.datetime.add_days(date, days);   // add n days to a date
// frappe.datetime.add_months(date, months); // add n months to a date
// frappe.datetime.month_end(date);  // returns the first day from the month of the given date
// frappe.datetime.month_start(date); // returns the last day from the month of the given date
// frappe.datetime.get_day_diff(begin, end); // returns the days between 2 dates
// https://discuss.erpnext.com/t/how-to-get-today-date/4554/17

// ModuleNotFoundError: No module named 'erpnext.projects.report.monthly_measurement_report.monthly_measurement_report'