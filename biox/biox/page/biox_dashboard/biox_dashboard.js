// https://discuss.erpnext.com/t/dynamic-custom-filter-in-reports/31567/11
// https://stackoverflow.com/questions/17610732/error-dictionary-update-sequence-element-0-has-length-1-2-is-required-on-dj
// https://github.com/frappe/erpnext/blob/develop/erpnext/accounts/report/account_balance/account_balance.js#L9
// https://github.com/frappe/frappe/blob/develop/frappe/public/js/frappe/views/reports/query_report.js
// https://codepen.io/Weldebob/pen/WjMLav
// https://stackoverflow.com/questions/6623231/remove-all-white-spaces-from-text
// https://css-tricks.com/auto-sizing-columns-css-grid-auto-fill-vs-auto-fit/
// https://stackoverflow.com/questions/931872/what-s-the-difference-between-array-and-while-declaring-a-javascript-ar// https://stackoverflow.com/questions/13792755/show-border-grid-lines-only-between-elements/47914693#47914693
// https://coder-coder.com/display-divs-side-by-side/
// https://stackoverflow.com/questions/14643617/create-table-using-javascript
// https://discuss.erpnext.com/t/bring-data-into-html-field-in-the-doctype/14194/4
// https://discuss.erpnext.com/t/how-to-fetch-child-tables/12348/2
// https://alainber.medium.com/adventures-with-frappe-charts-and-erpnext-pages-15cf2c5c562b
// https://discuss.erpnext.com/t/link-to-a-report/19091
// https://discuss.erpnext.com/t/number-format-explanation/30501
// https://discuss.erpnext.com/t/how-to-create-a-simple-html-table-and-load-the-content-from-the-other-doctype/10628/2
// https://github.com/frappe/charts
// https://discuss.erpnext.com/t/frappe-charts-in-page/44213/6
// https://frappe.io/charts/docs
frappe.provide("frappe.utils")
frappe.provide("frappe.charts")

var dt_to = new Date()
var dt_from = new Date(dt_to.getFullYear(),dt_to.getMonth()-6,1)
var html_grids_per_row=3

frappe.pages['biox-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'BIOX SUMMARY',
        single_column: true
    });
    var filters= {
        'from_date': dt_from,
        'to_date': dt_to,
        'customer':''
        }
    // console.log(filters)
 let from_date = page.add_field({
    label: 'From Date',
    fieldtype: 'Date',
    fieldname: 'from_date',
    default: dt_from,
    change() { 
            filters.from_date=from_date.get_value()
            frappe.biox_dashboard.run(page, filters);
        }
    });

    let to_date = page.add_field({
    label: 'To Date',
    fieldtype: 'Date',
    fieldname: 'to_date',
    default: dt_to,
    change() { 
        filters.to_date=to_date.get_value()
        frappe.biox_dashboard.run(page, filters);
        }   
    });   
    
    let customer = page.add_field({
    label: 'Customer',
    fieldtype: 'Link',
    options: 'Customer',
    fieldname: 'customer',
    change() 
        { 
            filters.customer=customer.get_value()
            frappe.biox_dashboard.run(page, filters);
        }
    });   


	frappe.biox_dashboard.make(page);
	frappe.biox_dashboard.run(page, filters);
    // console.log(page)
    // add the application reference
    frappe.breadcrumbs.add("Biox Dashboard");
    // console.log(frappe.db.count("Project", filters={"status":"Open"}))
}

frappe.biox_dashboard = {
	start: 0,
	make: function(page) {
		var me = frappe.biox_dashboard;
		me.page = page;
		me.body = $('<div></div>').appendTo(me.page.main);
		var data = "";
		$(frappe.render_template('biox_dashboard', data)).appendTo(me.body);
        // console.log("Data:")
        // console.log(data)
        // console.log("me:")
        // console.log(me)

	},
	run: function(page, filters) {
        get_project_stats(page,filters);
        master_data_issues(page, filters);
        get_lab_test_charts(page,filters);
        // get_montly_volume(page);
        // get_quotations_py(page);
        // get_sales_orders_py(page);
        // get_sales_invoices_py(page);
	}
}

function get_project_stats(page, filters) {
    frappe.call({
        "method": "biox.biox.page.biox_dashboard.biox_dashboard.get_project_stats",
        "args":{
            'filters': filters
        },
        "callback": function(r) {
            var container = page.main.find(".get_project_stats").empty();

            // console.log("CALLBACK")
            // console.log(r.message)
            if (r.message) {
                $('<h6 align=left>' + "Projects: " + r.message.project_count + '</h6>').appendTo(container);
                $('<h6 align=left>' + "Flow Measurements: " + frappe.format(r.message.flow_count, ) + '</h6>').appendTo(container);
                $('<h6 align=left>' + "Lab Tests: " + r.message.test_count + '</h6>').appendTo(container);
            } else {
                $('<h1>0</h1>').appendTo(container);
            }
        }
    });
}

function master_data_issues(page, filters) {
    frappe.call({
        "method": "biox.biox.page.biox_dashboard.biox_dashboard.master_data_issues",
        "args":{
            'filters': filters
        },
        "callback": function(r) {
            var container = page.main.find(".master_data_issues").empty();
            // console.log(r.message)
            if (r.message) {
                $('<h6 align = left><a href ='  + r.message.missing_cust_report_url + ' target="_blank">' + "Missing Sales Order : " + r.message.missing_so + '</a></h6>').appendTo(container);
                $('<h6 align = left><a href =' + r.message.improper_test_ranges_report_url + ' target="_blank" rel="noopener noreferrer">'+ "Verify Test Ranges : " + r.message.improper_test_ranges + '</a></h6>').appendTo(container);
                $('<h6 align = left><a href =' + r.message.duplicate_lab_test_structure_report_url + ' target="_blank" rel="noopener noreferrer">'+ "Duplicate Test Structures : " + r.message.duplicate_lab_test_structure + '</a></h6>').appendTo(container);
                $('<h6 align = left><a href =' + r.message.missing_customer_contract_no_report_url + ' target="_blank" rel="noopener noreferrer">'+ "Missing Customer Contract No :"  + r.message.missing_customer_contract_no + '</a></h6>').appendTo(container);
            } else {                 
                $('<h1>0</h1>').appendTo(container);
            }
        }   
    });
}

function get_lab_test_charts(page, filters) {
    frappe.call({
        "method": "biox.biox.page.biox_dashboard.biox_dashboard.get_lab_test_charts",
        "args":{
            'filters': filters
        },
        "callback": function(r) {
            if(r.message){
                // console.log(r.message)
                var container = page.main.find(".grid-wrapper").empty();
                // console.log(container)
                let tmpProj=r.message[1].project
                let chart_tag= ""
                let upper_range=0
                let lower_range = 0
                let chart_data={}
                let ispacer=0
                $.each(r.message, function(i,d){
                    // console.log(d)
                    // console.log(i)
                    ispacer+=1
                    if(tmpProj != d.project){
                        tmpProj=d.project;  
                        // console.log(i)
                        console.log(ispacer)
                        // project (tss/flow/etc) data is kept as a group. Once project changes start at a new line
                        // html_grids_per_row is the number of graphs that will be shown in a row. Hardcoded in biox_dashboard.html
                        // TODO: find a way to not hardcode this
                        for(let j=1; j<= html_grids_per_row-(ispacer-1)%html_grids_per_row;j++){    
                            container.append(`<div></div>`);
                        }
                        ispacer=1

                    }

                    chart_tag= d.project.replace(/\s/g,'') + d.parameter.replace(/\s/g,'')
                    upper_range=d.upper_range[d.upper_range.length-1]
                    lower_range = d.lower_range[d.lower_range.length-1]
                    chart_data={}
                    if(d.parameter == 'Volume'){
                        chart_data={
                            labels:d.month,
                            datasets: [
                                        {   'name': 'Volume',
                                            'values': d.month_result,
                                            'chart_type': 'line',
                                            lineoptions:{dotSize: 8, hideDots: 0}
                                        },
                                        {   'name': '30 x Daily Avg',
                                            'values': d.daily_average,
                                            'chart_type': 'bar'
                                        }
                                    ]
                            }
                    } else {
                        chart_data={
                            labels:d.month,
                            datasets: [{ 
                                        'values': d.month_result, 
                                        'chart_type': 'line'
                                    }],
                            yRegions: [
                                    {
                                        label: "Contractual Range",
                                        start: lower_range,
                                        end: upper_range,
                                        options: { labelPos: 'right' }
                                    }
                                ],

                            }
                    }
                    
                    // console.log(chart_data)
                    // console.log(chart_tag)
                    container.append(`<div id= "` + chart_tag + `"></div>`)
                    let graph = new frappe.Chart("#"+ chart_tag, {
                                        title: "Project: " + d.project + ", Parameter: " + d.parameter,
                                        data: chart_data,
                                        type: 'axis-mixed', 
                                        height: 250,
                                        colors: ['#7cd6fe', '#743ee2']

                                        
                        })            
                })
            }
        }
    })
}

// var container = page.main.find(".project_test_results").empty();
// 

//          // let chart_data = {
            //                 labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            //                 datasets: [
            //                         {
            //                             values:['0','10','20','30','40','50','60','70','50','40','30','20']
            //                         }
            //                     ]
            //                 };

            //                let graph = new frappe.Chart("#c1", {
            //                     title: "Test Results",
            //                     data: chart_data,
            //                     type: 'axis-mixed', // or 'bar', 'line', 'scatter', 'pie', 'percentage'
            //                     height: 250,
            //                     colors: ['#7cd6fd', '#743ee2']
            //                 });
            // // container.append(`<div id="test_chart1"></div>`);
            // let graph1 = new frappe.Chart("#c2", {
            //                         title: "Test Results1",
            //                         data: chart_data,
            //                         type: 'axis-mixed', // or 'bar', 'line', 'scatter', 'pie', 'percentage'
            //                         height: 250,
            //                         colors: ['#7cd6fe', '#743ee2']
                
            //     // var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td>rows[row][col]</td>{% } %}</tr>{% } %}</tbody></table>",
            //     // frm.set_df_property('html_fieldname', 'options', frappe.render(template, {rows: res.message});
            //     // frm.refresh_field('html_fieldname');
            // });

            // for (let i = 1; i < 10; i++) {
            //     container.append(`<div class="grid-box" id=` + "c" + i + ` green>  i:` + i +` </div>`);
            //     // container.append(`<div class="grid-container" id=` + "c" + 10*i + `> next box:` + 10*i +` </div>`);
            // }