// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
// https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/client_statement.js
// Sample report
// # Satish Vijayan 6/3/21
// https://github.com/frappe/datatable/issues/59
// https://maheshlangote.blogspot.com/2018/02/how-to-add-dynamic-columns-in-custom.html

var d = new Date();
var d1 = new Date(d.getFullYear(),d.getMonth()-1,1);


frappe.query_reports["Monthly Measurement Report"] = {
	on_change: function(report) {
	    report.page.add_inner_button(__("to_print"), function() {
			var selected_rows = [];
  			$('.dt-scrollable').find(":input[type=checkbox]").each((idx, row) => {
  				if(row.checked){
			         console.log("*** selected row id : " + idx);
			         selected_rows.push(frappe.query_report.data[$(row.closest(".dt-cell")).data("row-index")]);
				}
			});
		});
	},

    get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true
        });
    },

	"filters": [
		
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
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
			"default": frappe.datetime.add_days(frappe.datetime.add_months(d1,1),-1),
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