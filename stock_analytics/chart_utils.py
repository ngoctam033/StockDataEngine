import plotly.graph_objs as go
import plotly.io as pio

def create_line_chart(x, y_list, labels=None, title="Line Chart", xaxis_title="X Axis", yaxis_title="Y Axis", bullish_signals=None, bearish_signals=None):
    """
    Tạo một line chart với nhiều line và trả về dưới dạng HTML.
    
    Args:
        x (list): Dữ liệu trục X.
        y_list (list of lists): Danh sách các danh sách dữ liệu trục Y cho mỗi line.
        labels (list): Danh sách các nhãn cho mỗi line.
        title (str): Tiêu đề của biểu đồ.
        xaxis_title (str): Tiêu đề trục X.
        yaxis_title (str): Tiêu đề trục Y.
        bullish_signals (list of tuples): Danh sách các điểm Bullish Signal (ngày, giá trị).
        bearish_signals (list of tuples): Danh sách các điểm Bearish Signal (ngày, giá trị).
    
    Returns:
        str: Biểu đồ dưới dạng HTML.
    """
    fig = go.Figure()
    
    # Nếu không có nhãn, tạo nhãn mặc định
    if labels is None:
        labels = [f'Line {i+1}' for i in range(len(y_list))]
    
    # Thêm các line vào biểu đồ
    for y, label in zip(y_list, labels):
        fig.add_trace(go.Scatter(
            x=x, 
            y=y, 
            mode='lines', 
            name=label,
            hovertemplate='<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>',
            text=[label] * len(x)  # Thêm nhãn vào hover text
        ))
    
    # Thêm Bullish Signal
    if bullish_signals:
        bullish_dates, _ = zip(*bullish_signals)
        bullish_values = [y_list[0][x.index(date)] for date in bullish_dates]
        
        fig.add_trace(go.Scatter(
            x=bullish_dates, 
            y=bullish_values, 
            mode='markers', 
            name='Bullish Signal',
            marker=dict(color='green', size=10, symbol='triangle-up'),
            hovertemplate='Date: %{x}<br>Bullish Signal: %{y}<extra></extra>'
        ))

    # Thêm điểm Bearish Signal
    if bearish_signals:
        bearish_dates, _ = zip(*bearish_signals)
        bearish_values = [y_list[0][x.index(date)] for date in bearish_dates]
        fig.add_trace(go.Scatter(
            x=bearish_dates, 
            y=bearish_values, 
            mode='markers', 
            name='Bearish Signal',
            marker=dict(color='red', size=10, symbol='triangle-down'),
            hovertemplate='Date: %{x}<br>Bearish Signal: %{y}<extra></extra>'
        ))
 
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        ),
        dragmode='zoom',  # Chế độ kéo để zoom
        hovermode='closest',  # Chế độ hover gần nhất
        margin=dict(l=0, r=0, t=0, b=0),  # Lề
        legend=dict(
            x=0,  # Đặt vị trí của legend sang bên trái
        )
    )
    
    # Thêm chức năng zoom khi lăn chuột
    html_chart = pio.to_html(fig, full_html=False, config={'scrollZoom': True})
    return html_chart