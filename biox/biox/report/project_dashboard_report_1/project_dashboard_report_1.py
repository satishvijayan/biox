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
	
	if not filters.get('project'): 
		#frappe.throw(_("Please Select Project"))
		columns, data = [], []

	else:
		columns = get_columns(filters)
		data = get_data(filters)
	
	return columns, data


def get_columns(filters):
	return [
		
		{
			"fieldname": "measurement_date__time",
			"label": _("Measurement Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "calculated_daily_volume",
			"label": _("Daily Volume"),
			"fieldtype": "float",
			"width": 120
		},
		
		{
			"fieldname": "num_readings",
			"label": _("Number of Readings Taken"),
			"fieldtype": "int",
			"width": 100
		},
		{
			"fieldname": "site_gps_image",
			"label": _("Image File Location"),
			"fieldtype": "data",
			"width": 100
		},

	]

def get_data(filters):
	
	filter_doc_status = """ (0, 1) """ if filters.show_drafts == 1 else """ (1)""" ;

	s_sql =	f""" select  
						project 
						, date_format(measurement_date__time,"%%Y-%%m-%%d") as measurement_date__time 
						, format(avg(calculated_daily_volume),2) as calculated_daily_volume
						, count(calculated_daily_volume) as num_readings
						, site_gps_image  
					from `tabWater Height Measurement`  tw1
					where 
					project = \'{filters['project']}\'
					and tw1.docstatus in {filter_doc_status}
					and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
					group by project, date_format(measurement_date__time,"%%Y-%%m-%%d")   
					order by project, measurement_date__time 
			""";
	print(s_sql);
	return frappe.db.sql(s_sql,filters, as_dict=1)