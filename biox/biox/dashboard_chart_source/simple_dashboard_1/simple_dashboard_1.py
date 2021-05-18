# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, json
from frappe import _
from frappe.utils import add_to_date, date_diff, getdate, nowdate, get_last_day, formatdate, get_link_to_form
from frappe.utils.dashboard import cache_source
from frappe.utils.dateutils import get_from_date_from_timespan, get_period_ending
from frappe.utils.nestedset import get_descendants_of

@frappe.whitelist()
@cache_source
def get(chart_name=None, chart=None, no_cache=None, filters=None, from_date=None, to_date=None, timespan=None, time_interval=None, heatmap_year=None):
    if chart_name:
        chart = frappe.get_doc('Dashboard Chart', chart_name)
    else:
        chart = frappe._dict(frappe.parse_json(chart))

    
    chart_title="All"
    # frappe.msgprint(filters)
    if not filters:
        filters={}
        customer=None

    else:
        filters = frappe.parse_json(filters)
        customer = filters.get("customer")
        chart_title=customer

    projects = list()
    # frappe.msgprint(customer)
    projects = get_project_for_customer(customer)

    # axis label and data container is a list.
    axis_labels = []
    flow_measurements = []
    num_readings = []
    flow_measurements, num_readings, axis_labels = get_flow_measurement(projects, filters)

    

    # axis_labels = get_dates_from_timegrain(from_date, to_date, timegrain)
    return {
        'labels': axis_labels,
        'datasets': [
            {
                'name': 'Project Volume',

                'values': flow_measurements

             }
        ],
        'type': 'bar',
        'title': chart_title
    }


# returns a dict with the name of the project and associated values for each reporting period
@frappe.whitelist()
def get_flow_measurement(projects, filters):
    # frappe.msgprint(projects)
    filter_doc_status = """ (0, 1) """ if filters['show_drafts'] == 1 else """ (1)"""
    filter_projects = "('" + "', '".join([row['name'] for row in projects]) + "')"

    # frappe.msgprint(filters['to_date'])
    # frappe.msgprint(filters['from_date'])
    # frappe.msgprint(filter_projects)

    s_sql = f"""
                select  
                twm.customer
                , twm.project  as project
                , format(sum(twm.calculated_daily_volume),1)  as monthly_volume
                , sum(twm.num_readings) as num_readings
                from ( 
                        select  
                            customer
                            , project 
                            , date_format(measurement_date__time,"%%Y-%%m-%%d") as measurement_date__time 
                            , format(avg(calculated_daily_volume),4) as calculated_daily_volume 
                            , count(calculated_daily_volume) as num_readings  
                        from `tabWater Height Measurement`  tw1
                        where 
                        tw1.docstatus in {filter_doc_status}
                        and tw1.project in {filter_projects}
                        and tw1.measurement_date__time between \'{filters['from_date']}\' and \'{filters['to_date']}\'
                        group by customer, project, date_format(measurement_date__time,"%%Y-%%m-%%d")
                        order by customer, project, measurement_date__time 
                        
                    )
                as twm
                group by customer, project
                order by customer, project
                """

    # frappe.msgprint(s_sql);
    datasets = frappe.db.sql(s_sql, as_dict=1)
    # print(datasets)
    s1= ", '".join(row['project'] for row in datasets)
    #frappe.msgprint(s1)
    # frappe.msgprint(frappe.parse_json(datasets[0]['project']))

    # axis_labels_dict=dict()
    axis_labels = list() 
    flow_volume_list = list() 
    num_readings_list = list()
    i=0
    # list of projects and volume for the period
    for row in datasets:
        axis_labels.append("'"+ row['project'] + "'")
        flow_volume_list.append(row['monthly_volume'])
        num_readings_list.append(row['num_readings'])

    return flow_volume_list, num_readings_list, axis_labels


def get_list_of_lab_tests(from_date, to_date, projects):
    return


def get_project_for_customer(customer_name=None):
    if customer_name:
        projects = frappe.db.get_all(
            'Project',
            fields=['name'],
            filters=[dict(customer=('like', customer_name))],
            order_by='name asc'
        )
    else:
        projects = frappe.db.get_all(
            'Project',
            fields=['name'],
            order_by='customer asc, name asc'
        )

    # frappe.msgprint(customer_name)
    # frappe.msgprint(projects)
    return projects


def get_dates_from_timegrain(from_date, to_date, timegrain):
    days = months = years = 0
    if "Daily" == timegrain:
        days = 1
    elif "Weekly" == timegrain:
        days = 7
    elif "Monthly" == timegrain:
        months = 1
    elif "Quarterly" == timegrain:
        months = 3

    dates = [get_period_ending(from_date, timegrain)]
    while getdate(dates[-1]) < getdate(to_date):
        date = get_period_ending(add_to_date(dates[-1], years=years, months=months, days=days), timegrain)
        dates.append(date)
    return dates
