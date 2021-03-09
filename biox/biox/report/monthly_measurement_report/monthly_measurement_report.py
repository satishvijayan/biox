# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
# Satish Vijayan 6/3/21
# https://github.com/pradeshc/erpnext/blob/client_statement/erpnext/accounts/report/client_statement/client_statement.py
# https://discuss.erpnext.com/t/script-report-adding-columns-doesnt-reflect/45173/4

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
			"fieldtype": "Datetime",
			"width": 200
		},
		{
			"fieldname": "site_gps_image",
			"label": _("Site GPS Image"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "calculated_daily_volume",
			"label": _("Daily Volume"),
			"fieldtype": "float",
			"width": 120
		}
	]

def get_data(filters):
	
	return frappe.db.sql("""
		select 
			measurement_date__time, site_gps_image, calculated_daily_volume 
			from `tabWater Height Measurement` twm 
			where 
				twm.docstatus=1
				and twm.measurement_date__time <= %(to_date) s
				and twm.measurement_date__time >= %(from_date) s
				and twm.project like %(project) s

		 """,filters, as_dict=1)