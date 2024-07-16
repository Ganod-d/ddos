import requests

# URL mẫu để thử nghiệm (ví dụ là một URL có thể bị từ chối truy cập)
url = 'https://4gchill.com'

# Proxy và User Agent cụ thể
proxy = '103.41.32.182:58080'
user_agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'

# Hiển thị thông báo sử dụng proxy và user agent
print(f"Đang sử dụng Proxy: {proxy}")
print(f"Đang sử dụng User-Agent: {user_agent}")

# Tạo session requests với proxy và user agent cụ thể
session = requests.Session()
session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
session.headers = {'User-Agent': user_agent}

try:
    # Gửi yêu cầu HTTP GET với proxy và user agent đã chọn
    response = session.get(url)
    
    # Kiểm tra mã trạng thái của response
    if response.status_code == 200:
        print("Response:")
        print(response.text)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Request error: {e}")
