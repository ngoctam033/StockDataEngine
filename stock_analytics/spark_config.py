from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# địa chỉ của spark master
SPARK_MASTER = "spark://spark-master:7077"

def create_spark_session():
    """
    Tạo và trả về một SparkSession với các cấu hình cần thiết.
    """
    spark = SparkSession.builder \
        .appName("Stock Analysis") \
        .master(SPARK_MASTER) \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.cores", "4") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()
    
    return spark