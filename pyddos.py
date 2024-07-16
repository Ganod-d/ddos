import requests

# URL mẫu để thử nghiệm
url = 'https://httpbin.org/user-agent'

# Proxy và User Agent cụ thể
proxy = '103.41.32.182:58080'
user_agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'

# Tạo session requests với proxy và user agent cụ thể
session = requests.Session()
session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
session.headers = {'User-Agent': user_agent}

try:
    # Gửi yêu cầu HTTP GET với proxy và user agent đã chọn
    response = session.get(url)
    
    # Kiểm tra và in kết quả
    if response.status_code == 200:
        print(f"Proxy: {proxy}")
        print(f"User-Agent: {user_agent}")
        print("Response:")
        print(response.text)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Request error: {e}")
