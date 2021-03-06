insert into SE_Project.GraphByDay
SELECT d.number, d.name, (weekday(d.date_update)) as weekday, avg(d.available_bikes), avg(d.available_bike_stands), least(time_to_sec(d.time_update) div (60*60), 23)  as time_update 
FROM SE_Project.DynamicBike d
group by d.number, d.name, weekday(d.date_update), least(time_to_sec(d.time_update) div (60*60), 23);