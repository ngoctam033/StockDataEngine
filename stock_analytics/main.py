# import fastapi
from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
# import thư viện plotly để vẽ biểu đồ line chart
from chart_utils import create_line_chart
from spark_config import create_spark_session
from stock_analytics import read_csv, find_signals
import pandas as pd
#import thư viện để tính thời gian chạy hàm
import time

# tạo spark session
spark = create_spark_session()

# tạo ứng dụng FastAPI
app = FastAPI()

# Tạo hàm phụ trợ để trả về Spark session
# def get_spark_session():
#     return spark

# Tạo endpoint để in ra đồ thì line chart cổ phiếu
# bao gồm các thông tin: ngày, giá đóng cửa
@app.get("/stock/line_chart")
def line_chart(
    start_date: str = Query(..., description="Ngày bắt đầu (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Ngày kết thúc (YYYY-MM-DD)"),
    stock_symbol: str = Query(..., description="Mã cổ phiếu")):

    # bắt đầu tính thời gian chạy hàm
    start_time = time.time()

    #các trường dữ liệu cần thiết
    fields = ["Date", "Adj Close"] 
    # link file csv
    file_path = f"/app/stocks/{stock_symbol}.csv"

    # đọc dữ liệu từ file csv, sử dụng pandas
    df = pd.read_csv(file_path)

    # chọn các trường dữ liệu cần lấy
    df = df[fields]

    # Kiểm tra nếu start_date và end_date bằng 0 thì lấy tất cả dữ liệu
    if start_date != "0" and end_date != "0":
        # Lấy date từ start_date đến end_date
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    # tính toán MACD 6 ngày
    df["MACD_6"] = df["Adj Close"].ewm(span=6, adjust=False).mean()

    # tính toán MACD 13 ngày
    df["MACD_13"] = df["Adj Close"].ewm(span=13, adjust=False).mean()

    # tính toán MACD
    df["MACD"] = df["MACD_6"] - df["MACD_13"]

    # tính toán MACD Signal
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # chuyển đổi các trường sang list
    dates = df["Date"].tolist()
    close_prices = df["Adj Close"].tolist()
    MACD = df["MACD"].tolist()
    signal_line = df["MACD_Signal"].tolist()

    # tính các điểm Bullish Signal và Bearish Signal
    bullish_signals, bearish_signals = find_signals(dates, MACD, signal_line)

    html_line_chart = create_line_chart(dates, [close_prices, MACD, signal_line ], 
                                    labels=["Close Price", "MACD", "Signal Line"], 
                                    title=f"Stock Prices and MACD for {stock_symbol}",
                                    xaxis_title="Date", yaxis_title="Price",
                                    bullish_signals= bullish_signals,
                                    bearish_signals= bearish_signals)
    # kết thúc thời gian chạy hàm
    end_time = time.time()
    print(f"Time to run line_chart: {end_time - start_time} seconds")
    return HTMLResponse(content=html_line_chart)



