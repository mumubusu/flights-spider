create table flights (
id serial primary key,
company character varying(128),
flight_num character varying(128),
start_time character varying(128),
end_time character varying(128),
origin character varying(128),
destination character varying(128),
ori character varying(128),
des character varying(128)
)

CREATE TABLE public.airports
(
  id serial primary key,
  address character varying(128),
  lng character varying(128),
  lat character varying(128)
)

CREATE TABLE public.urls
(
  id serial primary key,
  url character varying(128),
  ori character varying(128),
  des character varying(128),
  ori_name character varying(128),
  des_name character varying(128),
  flag character varying(128)
)

copy flights to '/Users/petal02/Desktop/flights.csv' delimiter ',' csv HEADER