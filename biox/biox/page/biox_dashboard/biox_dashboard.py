# https://discuss.erpnext.com/t/set-multiple-fields-using-dict-javascript/40070/8
# https://gist.github.com/Tropicalrambler/53eec6b94cd0d7148116ffff54912057
# frappe.datetime.add_days(date, days);   // add n days to a date
# frappe.datetime.add_months(date, months); // add n months to a date
# frappe.datetime.month_end(date);  // returns the first day from the month of the given date
# frappe.datetime.month_start(date); // returns the last day from the month of the given date
# frappe.datetime.get_day_diff(begin, end)
# frappe.utils.today()
# frappe.utils.nowdate()
# https://frappeframework.com/docs/user/en/api/utils
# https://discuss.erpnext.com/t/how-to-get-today-date/4554/24
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from datetime import datetime
import collections

def foo():
    pass

def wrapstring(s):
    return "'" + str(s) + "'" if s else  ''

@frappe.whitelist()
def get_project_stats(filters):
    # sql_query = """SELECT COUNT(`name`) AS `count`
    #     FROM `tabProject` 
    #     WHERE `status` = 'Open' """
    # print(filters)
    if not filters:
        return
    else:
        filt = eval(filters)

    from_dt= wrapstring(filt['from_date'] )
    to_dt= wrapstring(filt['to_date'])
    customer=wrapstring(filt['customer'])
    
    if customer:
        cust_filt = " and p.customer = " + customer 
    else:
        cust_filt=""

    project_count = frappe.db.count("Project", filters={"status":"Open"})
    

    sql_query = f"""SELECT 
                        COUNT(whm.name) AS `count` 
                        from `tabWater Height Measurement` whm
                        left join tabProject p on p.name = whm.project
                        WHERE whm.docstatus in (0,1) 
                        AND measurement_date__time between {from_dt} AND {to_dt} 
                        {cust_filt} """
    flow_count = frappe.db.sql(sql_query,as_dict=True)
    sql_query = f"""SELECT 
                        COUNT(ltr.name) AS `count` 
                        from `tabLab Test Results` ltr
                        left join tabProject p on p.name = ltr.project
                        WHERE ltr.docstatus in (0,1) 
                        AND sample_date_time between {from_dt} AND {to_dt} 
                        {cust_filt} """
    test_count =  frappe.db.sql(sql_query, as_dict=True)
    
    return frappe._dict({
                'project_count': project_count,
                'flow_count': flow_count[0].count,
                'test_count': test_count[0].count
            })


# select tls1.project from (select project, count(project) as count from `tabLab Test Structure` tls where active = 1 group by project) tls1 where count > 1


@frappe.whitelist()
def master_data_issues(filters):
    if not filters:
        return
    else:
        filt = eval(filters)
   
    from_dt= wrapstring(filt['from_date'] )
    to_dt= wrapstring(filt['to_date'])
    customer=wrapstring(filt['customer'])

    if customer:
        cust_filt = " and p.customer = "+ customer  
    else:
        cust_filt=""

    
    sql_query = f"""select count(name) as count 
                    from tabProject 
                    where sales_order is null and status like 'Open' 
                    """
    missing_so = frappe.db.sql(sql_query, as_dict=True)
    missing_cust_report_url = frappe.utils.get_url_to_report(name='Missing Customer',report_type='Query Report', doctype='Project') 

    sql_query = """ select  
                        count(distinct project) as count
                        from `tabParameter Detail Values` tdv  
                        inner join `tabLab Test Structure` lts on tdv.parent=lts.name  
                        inner join tabProject p on lts.project=p.name  
                        where  
                        (tdv.upper_range=0 and tdv.lower_range=0) 
                        or (tdv.upper_range < tdv.lower_range) 
                        and p.status='Open' """
    improper_test_ranges = frappe.db.sql(sql_query, as_dict=True)
    improper_test_ranges_report_url = frappe.utils.get_url_to_report(name='Improper Test Range',report_type='Query Report', doctype='Parameter Detail Values')

    sql_query = """ select count(project) as count from       
                        (select project, count(name) as count 
                        from `tabLab Test Structure` where active=1 group by project) lts       
                    where lts.count > 1; """
    duplicate_lab_test_structure = frappe.db.sql(sql_query, as_dict=True)
    duplicate_lab_test_structure_report_url = frappe.utils.get_url_to_report(name='Duplicate Lab Test Structures',report_type='Query Report', doctype='Lab Test Structure')    

    return frappe._dict({
            'missing_so': missing_so[0].count,
            'missing_cust_report_url': missing_cust_report_url,
            'improper_test_ranges': improper_test_ranges[0].count,
            'improper_test_ranges_report_url': improper_test_ranges_report_url,
            'duplicate_lab_test_structure': duplicate_lab_test_structure[0].count,
            'duplicate_lab_test_structure_report_url': duplicate_lab_test_structure_report_url
        })

    

@frappe.whitelist()
def get_lab_test_charts(filters):
    
    if not filters:
        return
    else:
        filt = eval(filters)

    # print(filt)
    from_dt= wrapstring(filt['from_date'] )
    to_dt= wrapstring(filt['to_date'])
    customer=wrapstring(filt['customer'])

    #defining customer filter, outlet and water flow measurements
    if customer:
        cust_filt = " and p.customer = "+ customer 
    else:
        cust_filt=""


    sampling_filt= wrapstring("Outlet")
    water_flow_name='Volume'

    # print(date_labels)
    sql_query = f"""
                    select dash.*, round(dash.month_result/dash.num_samples,2) as daily_average
                    from(
                        select 
                            ltr.project as project
                            , date_format(ltr.sample_date_time, \'%%Y-%%m\') as month
                            , prv.parameter as parameter
                            , pdv.upper_range as upper_range
                            , pdv.lower_range as lower_range
                            , round(avg(prv.test_value),2) as month_result
                            , prv.uom as uom
                            , count(prv.test_value) as num_samples
                        from `tabLab Test Results` ltr
                        left join `tabParameter Result Values` prv on ltr.name=prv.parent
                        left join `tabLab Test Structure` lts on lts.project = ltr.project
                        left join `tabParameter Detail Values` pdv on pdv.parent = lts.name and prv.parameter = pdv.parameter
                        left join tabProject p on p.name = ltr.project
                        where 
                            pdv.contractually_required=1
                            and sampling_location = {sampling_filt}
                            and lts.active = 1 
                            and ltr.sample_date_time between {from_dt} and {to_dt}
                            and ltr.docstatus in (0,1)
                            {cust_filt}
                        group by project, parameter, UOM, month
                        

                        union

                        select 
                            dly.project as project
                            , date_format(dly.Measurement_day, "%%Y-%%m") as month
                            , \'{water_flow_name}\' as parameter 
                            , 0 as upper_range
                            , 0 as lower_range
                            , round(sum(calculated_daily_volume),0) as month_result
                            , "MLD" as UOM
                            , count(calculated_daily_volume) as num_samples
                        from 
                        (
                            select  
                                tw1.project , 
                                date_format(tw1.measurement_date__time,\'%%Y-%%m-%%d\') as Measurement_day , 
                                avg(calculated_daily_volume) as calculated_daily_volume 
                            from `tabWater Height Measurement`  tw1
                            left join tabProject p on p.name=tw1.project
                            where 
                                tw1.docstatus in (0,1)
                                and tw1.measurement_date__time between {from_dt} and {to_dt}
                                {cust_filt}
                            group by project, Measurement_day
                        ) dly 
                        group by project, Month
                    ) dash order by project, parameter, month

                    """ ;
    
    print(sql_query)
    data = frappe.db.sql(sql_query,{}, as_dict=1)

    chart_dict=proj_dict=month_dict=param_dict={}
    tmp_proj = tmp_month=tmp_parm=""
    iproj=imonth=iparam=0
    for rows in data:
        if rows.project != tmp_proj or rows.parameter!=tmp_parm:
            iproj+=1
            iparam+=1
            tmp_proj=rows.project
            tmp_parm=rows.parameter
            chart_dict.update({iproj: {'project': rows.project , 'parameter': rows.parameter,'month':[], 'month_result':[], 'color':[], 'upper_range':[], 'lower_range':[], 'daily_average':[] } })
            

        chart_dict[iproj]['month'].append(rows.month)
        chart_dict[iproj]['month_result'].append(float(rows.month_result))
        chart_dict[iproj]['upper_range'].append(rows.upper_range)
        chart_dict[iproj]['lower_range'].append(rows.lower_range)
        chart_dict[iproj]['daily_average'].append(rows.daily_average)
        value_color = 'black' if float(rows.lower_range) <= float(rows.month_result) <= float(rows.upper_range) else 'red'
        chart_dict[iproj]['color'].append(value_color)
    
    return chart_dict

        
@frappe.whitelist()
def get_sales_invoices_ytd():
    sql_query = """SELECT COUNT(`name`) AS `count`, IFNULL(SUM(`base_grand_total`), 0) AS `sum`
        FROM `tabSales Invoice` 
        WHERE `docstatus` = 1 AND `posting_date` >= '{0}-01-01' AND `posting_date` <= '{1}'""".format(
        datetime.now().year, 
        datetime.now().date())
    print(sql_query)
    invoices = frappe.db.sql(sql_query, as_dict=True)
    if invoices:
        return {'invoices': invoices[0] }
    else:
        return {'invoices': 'None' }

@frappe.whitelist()
def get_quotations_py():
    sql_query = """SELECT COUNT(`name`) AS `count`, IFNULL(SUM(`base_grand_total`), 0) AS `sum`
        FROM `tabQuotation` 
        WHERE `docstatus` = 1 AND `transaction_date` >= '{0}-01-01' AND `transaction_date` <= '{0}-{1}-{2}'""".format(
        (datetime.now().year - 1),
        datetime.now().month, datetime.now().day)
    print(sql_query)
    quotations = frappe.db.sql(sql_query, as_dict=True)
    if quotations:
        return {'quotations': quotations[0] }
    else:
        return {'quotations': 'None' }

@frappe.whitelist()
def get_sales_orders_py():
    sql_query = """SELECT COUNT(`name`) AS `count`, IFNULL(SUM(`base_grand_total`), 0) AS `sum`
        FROM `tabSales Order` 
        WHERE `docstatus` = 1 AND `transaction_date` >= '{0}-01-01' AND `transaction_date` <= '{0}-{1}-{2}'""".format(
        (datetime.now().year - 1),
        datetime.now().month, datetime.now().day)
    print(sql_query)
    orders = frappe.db.sql(sql_query, as_dict=True)
    if orders:
        return {'orders': orders[0] }
    else:
        return {'orders': 'None' }
        
@frappe.whitelist()
def get_sales_invoices_py():
    sql_query = """SELECT COUNT(`name`) AS `count`, IFNULL(SUM(`base_grand_total`), 0) AS `sum`
        FROM `tabSales Invoice` 
        WHERE `docstatus` = 1 AND `posting_date` >= '{0}-01-01' AND `posting_date` <= '{0}-{1}-{2}'""".format(
        (datetime.now().year - 1),
        datetime.now().month, datetime.now().day)
    print(sql_query)
    invoices = frappe.db.sql(sql_query, as_dict=True)
    if invoices:
        return {'invoices': invoices[0] }
    else:
        return {'invoices': 'None' }



# for rows in data:
    #     if rows.month != tmp_month:
    #         chart_dict.update({rows.month : {}})
    #         month_dict.update({imonth: rows.month})
    #         imonth+=1

    #         chart_dict[rows.month].update({rows.project:{}})
    #         if rows.project not in proj_dict.values():
    #             proj_dict.update({iproj : rows.project})
    #             iproj+=1

    #     if rows.parameter != tmp_parm:
    #         chart_dict[rows.month][rows.project].update({rows.parameter : {}})
    #         if rows.parameter not in param_dict.values():
    #             param_dict.update({iparam : rows.parameter})

        # chart_dict[rows.month][rows.project][rows.parameter].update({"upper_range": rows.upper_range, "lower_range": rows.lower_range, "month_result":rows.month_result, "Num_Samples":rows.Num_Samples})
    # for rows in 
    #     # Project wise monthly test results
    #     month_list=list(month_dict.values())
    #     iproj=0
    #     data_dict={}
    #     for project in proj_dict:
    #         for month in month_dict:
                
    #             for param in param_dict:




        # print(rows.Month, rows.project, rows.parameter, rows.Month_Result, rows.Num_Samples)
        # chart_dict.append{rows.project : {rows.parameter: {"upper_range": rows.upper_range, "lower_range": rows.lower_range, "Month_Result":rows.Month_Result, "Num_Samples":rows.Num_Samples }} }

    # print(chart_dict)        