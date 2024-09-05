# import fastapi
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# import thư viện plotly để vẽ biểu đồ line chart
from chart_utils import create_line_chart
from spark_config import create_spark_session

# tạo spark session
spark = create_spark_session()

# tạo ứng dụng FastAPI
app = FastAPI()
# Tạo endpoint để in ra đồ thì line chart cổ phiếu
@app.get("/stock/line_chart")
def line_chart():
    # Dữ liệu mẫu
    dates = ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"]
    open_prices = [100, 102, 101, 105, 107]
    close_prices = [102, 101, 105, 107, 110]
    
    html_chart = create_line_chart(dates, [open_prices, close_prices], labels=["Open Price", "Close Price"], title="Stock Prices", xaxis_title="Date", yaxis_title="Price")
    return HTMLResponse(content=html_chart)



