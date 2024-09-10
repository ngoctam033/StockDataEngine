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
    # Định nghĩa hàm ewm để tính toán Exponential Weighted Moving Average
    def ewm(df, span):
        alpha = 2 / (span + 1)
        return df.withColumn("ewm", expr(f"SUM(Adj Close * {alpha} * (1 - {alpha}) ^ (ROW_NUMBER() OVER (ORDER BY Date) - 1)) OVER (ORDER BY Date)"))

    # Định nghĩa hàm ewm để tính toán Exponential Weighted Moving Average
    spark.udf.register("ewm", ewm)
    
    return spark

