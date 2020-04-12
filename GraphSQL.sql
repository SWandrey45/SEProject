-- Query to insert date into graph table grouped by station, and hour of the day
insert into SE_Project.Graph
SELECT d.number, d.name, avg(d.available_bikes), avg(d.available_bike_stands), least(time_to_sec(d.time_update) div (60*60), 23)  as time_update 
FROM SE_Project.DynamicBike d
group by d.number, d.name, least(time_to_sec(d.time_update) div (60*60), 23);