select 
		dly.project as project
		, date_format(dly.Measurement_day, "%Y-%m") as Month
		, format(sum(calculated_daily_volume),0) as Month_Result
		, "MLD" as UOM
		, count(calculated_daily_volume) as Num_Samples
		from (
			select project 
				, date_format(tw1.measurement_date__time,"%Y-%m-%d") as Measurement_day 
				, format(avg(calculated_daily_volume),2) as calculated_daily_volume 
			from `tabWater Height Measurement`  tw1 
			group by project, Measurement_day
		) dly 
	group by project, Month 
) Dash_report
left join tabProject p on Dash_report.project = p.name
where p.customer like {customer_filter}
order by p.customer, project, Month, parameter

 select dly.project, date_format(dly.Measurement_day, "%Y-%m") as Month , format(sum(calculated_daily_volume),0) as Month_Volume, count(calculated_daily_volume) as Num_Samples from ( select project  , date_format(tw1.measurement_date__time,"%Y-%m-%d") as Measurement_day, format(avg(calculated_daily_volume),2) as calculated_daily_volume  from `tabWater Height Measurement`  tw1 group by project, Measurement_day) dly group by project, Month ;


select ltr.project as 	project, date_format(sample_date_time, '%Y-%m') as Month, prv.parameter as parameter, format(avg(prv.test_value),2) as Month_Result, prv.uom as UOM, count(prv.test_value) as Num_Samples, format(avg(prv.test_value),2) as Daily_Average
					from `tabLab Test Results` ltr 
					left join `tabParameter Result Values` as prv on ltr.name=prv.parent
					group by project, Month,  parameter, UOM , sampling_location


select ltr.project as project, date_format(ltr.sample_date_time, '%Y-%m') as Month
, prv.parameter as parameter, pdv.upper_range, pdv.lower_range 
, format(avg(prv.test_value),2) as Month_Result, prv.uom as UOM
, count(prv.test_value) as Num_Samples
from `tabLab Test Results` ltr
left join `tabParameter Result Values` prv on ltr.name=prv.parent
left join `tabLab Test Structure` lts on lts.project = ltr.project
left join `tabParameter Detail Values` pdv on pdv.parent = lts.name and prv.parameter = pdv.parameter
where
pdv.contractually_required=1
and lts.active = 1
group by project, Month, parameter, UOM;


select lts.project, tbdv.parent, tbdv.parameter, tbdv.upper_range, tbdv.lower_range 
	from `tabParameter Detail Values` tbdv 
	inner join `tabLab Test Structure` lts on lts.name = tbdv.parent 




select 
	project, name as 'Test Structure'
from 
	`tabLab Test Structure` where project in 
    (select project from 
     	(select project, count(name) as count from `tabLab Test Structure` where active=1 group by project) lts 
     	where lts.count > 1) 
order by project;

select  
	lts.project, tdv.parent, tdv.parameter, tdv.upper_range, tdv.lower_range 
	from `tabParameter Detail Values` tdv  
	inner join `tabLab Test Structure` lts on tdv.parent=lts.name  
	inner join tabProject p on lts.project=p.name  
	where  
	(tdv.upper_range=0 and tdv.lower_range=0) 
	or (tdv.upper_range < tdv.lower_range) 
	and p.status='Open';