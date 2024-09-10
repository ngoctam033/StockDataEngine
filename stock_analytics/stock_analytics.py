# đây là file chứa các hàm phân tích dữ liệu của cổ phiếu
# các hàm này sẽ được gọi trong file main.py
from pyspark.sql.functions import col, expr, lit
from pyspark.sql.window import Window
# tạo một hàm để lấy các trường dữ liệu trong file csv, sử dụng spark
# đầu vào: spark session, đường dẫn file csv, tên các trường dữ liệu cần lấy
# đầu ra: dataframe chứa các trường dữ liệu cần lấy
def read_csv(spark, file_path, fields):
    """
    Đọc dữ liệu từ file CSV và trả về dưới dạng DataFrame.
    
    Args:
        spark (SparkSession): Spark session.
        file_path (str): Đường dẫn file CSV.
        fields (list): Danh sách các trường dữ liệu cần lấy.
    
    Returns:
        DataFrame: DataFrame chứa dữ liệu.
    """
    # Đọc dữ liệu từ file CSV, sử dụng pandas
    df = pd.read_csv(file_path)
    
    # Chọn các trường dữ liệu cần lấy
    df = df[fields]
    
    # chuyển đổi thành dataframe của spark
    df = spark.createDataFrame(df)

    return df

# Tạo hàm để tính các điểm Bullish Signal và Bearish Signal
def find_signals(dates, MACD, signal_line):
    bullish_signals = []
    bearish_signals = []

    for i in range(1, len(dates)):
        # kiểm tra xem giá trị macd tại thời điển i-1 và i
        #  MACD[i-1] < signal_line[i-1] và MACD[i] > signal_line[i] -> bullish signal
        if MACD[i-1] < signal_line[i-1] and MACD[i] > signal_line[i]:
            bullish_signals.append((dates[i], MACD[i]))
        #  MACD[i-1] > signal_line[i-1] và MACD[i] < signal_line[i] -> bearish signal
        elif MACD[i-1] > signal_line[i-1] and MACD[i] < signal_line[i]:
            bearish_signals.append((dates[i], MACD[i]))

    return bullish_signals, bearish_signals

def calculate_ema(spark_df, column, span):
    alpha = 2 / (span + 1)
    ema_column = f"EMA_{span}"
    window_spec = Window.orderBy("Date").rowsBetween(Window.unboundedPreceding, 0)
    spark_df = spark_df.withColumn(ema_column, expr(f"SUM({column} * {alpha} * POWER(1 - {alpha}, ROW_NUMBER() OVER ({window_spec}) - 1)) OVER ({window_spec})"))
    return spark_df