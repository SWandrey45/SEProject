-- Query to obtain the up-to-date weather information
select w.temp, w.humidity, w.description, w.icon, w.city, w.wind_speed, w.wind_direction
from SE_Project.Weather w, (select max(w1.date_update  + INTERVAL time_to_sec(w1.time_update) second) as updated from SE_Project.Weather w1) w2
where w.date_update + INTERVAL time_to_sec(w.time_update) second = w2.updated
