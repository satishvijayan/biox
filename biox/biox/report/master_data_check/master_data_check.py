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
			"fieldname": "Customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options":"Customer",
			"width": 100
		},
		{
			"fieldname": "Project_Name",
			"label": _("Project"),
			"fieldtype": "Link",
			"options":"Project",
			"width": 100
		},
		{
			"fieldname": "Created_on",
			"label": _("Created Date"),
			"fieldtype": "Date",
			"width": 80
		},
		{
			"fieldname": "Sales_Order",
			"label": _("Sales Order"),
			"fieldtype": "Link",
			"options":"Sales Order",
			"width": 100,
			"align":"right"
		},
		{
			"fieldname": "Lab_Structure",
			"label": _("Lab Structure"),
			"fieldtype": "Link",
			"options":"Lab Test Structure",
			"width": 80,
			"align":"middle"
		},
		{
			"fieldname": "Ht_Measurement_Count",
			"label": _("Flow Count"),
			"fieldtype": "int",
			"width": 80,
			"align":"right"
		},
		{
			"fieldname": "Lab_Test_Count",
			"label": _("Labs Count"),
			"fieldtype": "int",
			"width": 80,
			"align": "middle"
		},
		

	]

def get_data(filters):
	
	filter_doc_status = """ (0, 1) """ if filters.show_drafts == 1 else """ (1)""" ;
	project_filter = f"""  \'%%{filters.project}%%\' """  if filters.get('project')  else "\'%%\'";
	customer_filter = f"""  \'%%{filters.customer}%%\' """  if filters.get('customer')  else "\'%%\'";
	
	# frappe.msgprint(customer_filter);
	# frappe.msgprint(project_filter);
	
	#frappe.show_alert(project_filter + "|" + customer_filter, 20);
	
	
	s_sql =	f""" 
				select  
    				W.num_water as "Ht_Measurement_Count",
				    LTR.Num_Tests as "Lab_Test_Count" ,
				    p.customer as"Customer" , 
				    p.name as "Project_Name", 
				    date_format(p.creation,"%%y-%%m-%%d") `Created_on`, 
				    p.sales_order as "Sales_Order", 
				    lts.name as "Lab_Structure"
				from tabProject p 
				left join `tabLab Test Structure` lts  on p.name = lts.project 
				left join  
					(select project,  count(height) as Num_water 
						from `tabWater Height Measurement` tw1
						where 
							tw1.docstatus in {filter_doc_status} 
							and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
							group by project
					) W on p.name = W.project 
				left join 
					(select project, count(sample_date_time) as Num_Tests 
						from `tabLab Test Results` tlr1
						where 
							tlr1.docstatus in {filter_doc_status}
							and tlr1.sample_date_time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
							group by project
					) LTR on p.name = LTR.project

				where 
				p.customer like {customer_filter}
				and p.name like {project_filter}
				order by p.customer, p.name;


			""";
	
	# frappe.msgprint(s_sql);

	return frappe.db.sql(s_sql,filters, as_dict=1)


	# project = \'{filters['project']}\'
	#				and tw1.docstatus in {filter_doc_status}
	#				and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'