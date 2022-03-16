
Lab 1 -  Intro Pre-process

Clonando repo
```sh
git clone https://github.com/GoogleCloudPlatform/training-data-analyst 
```

copiando arquivo e salvando no storage
```py
!gsutil cp gs://cloud-training/mlongcp/v3.0_MLonGC/toy_data/untidy_vehicle_data_toy.csv ../data/transport
```


pegando primeira data de cada mês
```py
df_transport.groupby('Fuel').first() # Get the first entry for each month. 
```


https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/courses/machine_learning/deepdive2/launching_into_ml/solutions/improve_data_quality.ipynb


-------------------------------------------------------------------------------

Lab 2 - Análise de dados exploratória usando Python e BigQuery

Clonando repo
```sh
git clone https://github.com/GoogleCloudPlatform/training-data-analyst 
```


Etapa 1

Na interface do notebook, navegue até training-data-analyst > courses > machine_learning > deepdive2 > launching_into_ml > labs e abra python.BQ_explore_data.ipynb.

copiando arquivo e salvando no storage
```py
!gsutil cp gs://cloud-training/mlongcp/v3.0_MLonGC/toy_data/housing_pre-proc_toy.csv ../data/explore  
```

Usou Bigquery no Notebook

```sql
%%bigquery
SELECT
    FORMAT_TIMESTAMP(
        "%Y-%m-%d %H:%M:%S %Z", pickup_datetime) AS pickup_datetime,
    pickup_longitude, pickup_latitude, dropoff_longitude,
    dropoff_latitude, passenger_count, trip_distance, tolls_amount, 
    fare_amount, total_amount 
# TODO 3: Set correct BigQuery public dataset for nyc-tlc yellow taxi cab trips
# Tip: For projects with hyphens '-' be sure to escape with backticks ``
FROM
    `nyc-tlc.yellow.trips`
LIMIT 10
```
Retornando resposta no formato Dataframe chamado trips
```sql
%%bigquery trips
SELECT
    FORMAT_TIMESTAMP(
        "%Y-%m-%d %H:%M:%S %Z", pickup_datetime) AS pickup_datetime,
    pickup_longitude, pickup_latitude, 
    dropoff_longitude, dropoff_latitude,
    passenger_count,
    trip_distance,
    tolls_amount,
    fare_amount,
    total_amount
FROM
    `nyc-tlc.yellow.trips`
WHERE
    ABS(MOD(FARM_FINGERPRINT(CAST(pickup_datetime AS STRING)), 100000)) = 1
```

```sql
%%bigquery trips
SELECT
    FORMAT_TIMESTAMP(
        "%Y-%m-%d %H:%M:%S %Z", pickup_datetime) AS pickup_datetime,
    pickup_longitude, pickup_latitude, 
    dropoff_longitude, dropoff_latitude,
    passenger_count,
    trip_distance,
    tolls_amount,
    fare_amount,
    total_amount
FROM
    `nyc-tlc.yellow.trips`
WHERE
    ABS(MOD(FARM_FINGERPRINT(CAST(pickup_datetime AS STRING)), 100000)) = 1
    # TODO 4a: Filter the data to only include non-zero distance trips and fares above $2.50
    AND trip_distance > 0
    AND fare_amount >= 2.5
```