# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
# Satish Vijayan 6/3/21
# https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/client_statement.py
# https://discuss.erpnext.com/t/script-report-adding-columns-doesnt-reflect/45173/4
# https://github.com/frappe/datatable/issues/59
# https://discuss.erpnext.com/t/script-report-python-file-returns-advanced-use/33489/5
# https://discuss.erpnext.com/t/issue-with-treeview-in-frappe-datatable/45207/11
from __future__ import unicode_literals
import frappe
from frappe import _, _dict
from frappe import msgprint

def execute(filters=None):
	
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data


def get_columns(filters):
	return [
		
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "data",
			"width": 120
		},
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "data",
			"width": 120
		},
		{
			"fieldname": "Month",
			"label": _("Period"),
			"fieldtype": "data",
			"width": 80
		},
		{
			"fieldname": "parameter",
			"label": _("Parameter"),
			"fieldtype": "data",
			"width": 100
		},
		{
			"fieldname": "Month_Result",
			"label": _("Month Result"),
			"fieldtype": "float",
			"width": 100,
			"align":"right"
		},
		{
			"fieldname": "UOM",
			"label": _("UOM"),
			"fieldtype": "data",
			"width": 80,
			"align":"middle"
		},
		{
			"fieldname": "Num_Samples",
			"label": _("Samples Taken"),
			"fieldtype": "int",
			"width": 80,
			"padding": "0.75rem"
		},
		

	]

def get_data(filters):
	
	filter_doc_status = """ (0, 1) """ if filters.show_drafts == 1 else """ (1)""" ;
	project_filter = f"""  \'%%{filters.project}%%\' """  if filters.get('project')  else "\'%%\'";
	customer_filter = f"""  \'%%{filters.customer}%%\' """  if filters.get('customer')  else "\'%%\'";
	
	# frappe.msgprint(customer_filter);
	# frappe.msgprint(project_filter);
	
	#frappe.show_alert(project_filter + "|" + customer_filter, 20);
	water_flow_name = "Month Flow"
	
	s_sql =	f""" 
				select p.customer, Dash_report.* from 
				( 
					select 
						ltr.project as project, 
						date_format(sample_date_time,'%%Y-%%m') as Month, 
						prv.parameter as parameter, 
						format(avg(prv.test_value),2) as Month_Result,
						prv.uom as UOM,
						count(prv.test_value) as Num_Samples
					from `tabLab Test Results` ltr 
					left join `tabParameter Result Values` as prv on ltr.name=prv.parent
					where 
						ltr.docstatus in {filter_doc_status}
						and ltr.sample_date_time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
						and ltr.project like {project_filter}
					group by project, Month,  parameter, UOM 

				union

					select 
						dly.project as project, 
						date_format(dly.Measurement_day,"%%Y-%%m") as Month, 
						\'{water_flow_name}\' as parameter, 
						format(sum(calculated_daily_volume),0) as Month_Result, 
						"MLD" as UOM,
						count(calculated_daily_volume) as Num_Samples
					from 
					(
						select  
							project , 
							date_format(tw1.measurement_date__time,"%%Y-%%m-%%d") as Measurement_day , 
							format(avg(calculated_daily_volume),2) as calculated_daily_volume 
						from `tabWater Height Measurement`  tw1
						where 
							tw1.docstatus in {filter_doc_status}
							and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
							and tw1.project like {project_filter}
						group by project, Measurement_day
					) dly 
					group by project, Month 
				) Dash_report
				left join tabProject p on Dash_report.project = p.name
				where p.customer like {customer_filter}

			order by p.customer, project, Month, parameter

			""";
	
	# frappe.msgprint(s_sql);

	return frappe.db.sql(s_sql,filters, as_dict=1)


	# project = \'{filters['project']}\'
	#				and tw1.docstatus in {filter_doc_status}
	#				and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'