import json
from datetime import datetime
from pyspark.sql import SparkSession


spark=SparkSession.builder.appName('Spark_lab5').config("spark.some.config.option").getOrCreate()
sc=spark.sparkContext

try:

    data = sc.textFile("/home/vmdisk/data.txt")

    rides = data.map(lambda line: line.split(",")).filter(lambda row: row[12] != '').map(lambda row: (int(row[0]), float(row[12])))

    driver_ratings = rides.reduceByKey(lambda a, b: a + b)
    low_rated_drivers = driver_ratings.filter(lambda key_value: key_value[1] < 3.5)

    # for driver_id in low_rated_drivers.collect():
    #     print(driver_id)

    low_rated_drivers_dicts = low_rated_drivers.map(lambda key_value: {"driver_id": key_value[0], "rating": key_value[1]})

    with open("low_rated_drivers.json", "w") as f:
        json.dump(low_rated_drivers_dicts.collect(), f)

    print('[INFO] Completed')
except Exception as _ex:
    print(_ex)
finally:
    spark.stop()



    