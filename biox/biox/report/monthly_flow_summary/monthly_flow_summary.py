# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
# Satish Vijayan 6/3/21
# https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/client_statement.py
# https://discuss.erpnext.com/t/script-report-adding-columns-doesnt-reflect/45173/4
#     console.dir(frappe.datetime);
from __future__ import unicode_literals
import frappe
from frappe import _, _dict
from frappe import msgprint

def execute(filters=None):
	if not filters:
		return [], []	
	

	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	return [
		
		{
			"fieldname": "project",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "project",
			"width": 150
		},
		{
			"fieldname": "month",
			"label": _("Month / Year YYYY-MM"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "num_readings",
			"label": _("# of Entries"),
			"fieldtype": "int",
			"width": 120
		},
		{
			"fieldname": "monthly_volume",
			"label": _("Monthly Flow (MLD)"),
			"fieldtype": "float",
			"width": 120,
			"precision": 2
		},
		{
			"fieldname": "daily_avg_volume",
			"label": _("Daily Average (MLD)"),
			"fieldtype": "float",
			"width": 120,
			"precision": 2
		}
	]


def get_data(filters):
	
	filter_doc_status = """ (0, 1) """ if filters.show_drafts == 1 else """ (1)""" ;
	print(filter_doc_status);
	filter_cust = """ and tw1.customer = '""" + filters.customer + "'" if filters.customer else ""

	s_sql = f"""
			select  
			twm.project , date_format(twm.measurement_date__time, '%%Y-%%m') as month
 			, format(sum(twm.calculated_daily_volume),1)  as monthly_volume
 			, sum(twm.num_readings) as num_readings
 			, format(if( sum(twm.num_readings)>0, sum(twm.calculated_daily_volume)/sum(twm.num_readings),0),2)
 				as daily_avg_volume
 			from ( 
 					select  
						docstatus, project 
						, date_format(measurement_date__time,"%%Y-%%m-%%d") as measurement_date__time 
						, format(avg(calculated_daily_volume),4) as calculated_daily_volume 
						, count(calculated_daily_volume) as num_readings  
					from `tabWater Height Measurement`  tw1
					where 
					tw1.docstatus in {filter_doc_status}
					{filter_cust}
					and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
					group by project, date_format(measurement_date__time,"%%Y-%%m-%%d")
					order by project, measurement_date__time 
				)
			as twm 
			group by twm.project, month
			order by twm.project, month """;

	print(s_sql);
	return frappe.db.sql(s_sql,filters, as_dict=1)