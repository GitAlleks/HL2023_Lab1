import json
from datetime import datetime
from pyspark.sql import SparkSession


spark=SparkSession.builder.appName('Spark_lab5').getOrCreate()
sc=spark.sparkContext

try:



    data = sc.textFile("/home/vmdisk/data.txt")

    rides = data.map(lambda line: line.split(",")).filter(lambda row: row[12] != '').map(lambda row: (int(row[0]), (float(row[12]), 1)))

    driver_ratings = rides.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
    average_ratings = driver_ratings.map(lambda key_value: (key_value[0], key_value[1][0] / key_value[1][1]))
    low_rated_drivers = average_ratings.filter(lambda key_value: key_value[1] < 3.5)
    low_rated_drivers_dicts = low_rated_drivers.map(lambda key_value: {"driver_id": key_value[0], "average_rating": key_value[1]})

    with open("low_rated_drivers.json", "w") as f:
        json.dump(low_rated_drivers_dicts.collect(), f)


    print('[INFO] Completed')
except Exception as _ex:
    print(_ex)
finally:
    spark.stop()







data = sc.textFile("/home/vmdisk/data.txt")

rides = data.map(lambda line: line.split(",")).filter(lambda row: row[12] != '').map(lambda row: (int(row[0]), float(row[12])))

driver_ratings = rides.reduceByKey(lambda a, b: a + b) 

low_rated_drivers = driver_ratings.filter(lambda key_value: key_value[1] < 3.5)

low_rated_drivers_dicts = low_rated_drivers.map(lambda key_value: {"driver_id": key_value[0], "rating": key_value[1]})

# with open("low_rated_drivers.json", "w") as f:
#     json.dump(low_rated_drivers_dicts.collect(), f)
# average_driver_ratings = driver_ratings.mapValues(lambda x: x / rides.filter(lambda y: y[0] == x[0]).count())
# low_rated_drivers = average_driver_ratings.filter(lambda key_value: key_value[1] < 3.5)
# low_rated_drivers_dicts = low_rated_drivers.map(lambda key_value: {"driver_id": key_value[0], "rating": key_value[1]})
