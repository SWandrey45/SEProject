select s.number, s.name, s.address, s.position_lat, s.position_lng, d.bike_stands, d.available_bikes, d.available_bike_stands, d.status
from SE_Project.station s, SE_Project.DynamicBike d, (select d1.number, max(d1.date_update + INTERVAL time_to_sec(d1.time_update) second) as date_update from SE_Project.DynamicBike d1 group by d1.number) as d2
where s.number = d.number
and s.number = d2.number
and d.date_update + INTERVAL time_to_sec(d.time_update) second= d2.date_update;
