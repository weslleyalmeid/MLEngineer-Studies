Abra o Cloud Shell e execute o comando abaixo para criar o conjunto de dados taxirides.
```sh
bq mk taxirides
```


Execute este comando para criar a tabela taxirides.realtime (esquema vazio para o streaming).
```sh
bq mk \
--time_partitioning_field timestamp \
--schema ride_id:string,point_idx:integer,latitude:float,longitude:float,\
timestamp:timestamp,meter_reading:float,meter_increment:float,ride_status:string,\
passenger_count:integer -t taxirides.realtime
```

Schema mode text
```sh
ride_id:string,
point_idx:integer,
latitude:float,
longitude:float,
timestamp:timestamp,
meter_reading:float,
meter_increment:float,
ride_status:string,
passenger_count:integer
```