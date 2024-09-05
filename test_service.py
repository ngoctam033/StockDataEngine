import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(url):
    try:
        start_time = time.time()  # Bắt đầu đo thời gian
        response = requests.get(url)
        end_time = time.time()  # Kết thúc đo thời gian
        
        elapsed_time = end_time - start_time  # Tính thời gian đã trôi qua
        
        if response.status_code == 200:
            print(f"Success")
        else:
            print(f"Failed with status code {response.status_code}")
        
        print(f"Request took {elapsed_time:.2f} seconds")
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred - {e}")

if __name__ == "__main__":
    url = "http://localhost/api/data"
    num_requests = 1000  # Số lượng yêu cầu muốn gửi
    delay = 0  # Thời gian chờ giữa các yêu cầu (tính bằng giây)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_data, url) for _ in range(num_requests)]
        
        for future in as_completed(futures):
            future.result()  # Đợi cho mỗi yêu cầu hoàn thành