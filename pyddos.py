import random
import requests

# Đọc dữ liệu từ proxy.txt
def read_proxy_file(filename):
    proxies = []
    try:
        with open(filename, 'r') as file:
            proxies = file.read().splitlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return proxies

# Đọc dữ liệu từ ua.txt
def read_user_agents_file(filename):
    user_agents = []
    try:
        with open(filename, 'r') as file:
            user_agents = file.read().splitlines()
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return user_agents

# Chọn ngẫu nhiên một proxy và một user agent
def get_random_proxy(proxies):
    return random.choice(proxies)

def get_random_user_agent(user_agents):
    return random.choice(user_agents)

# URL mẫu để thử nghiệm
url = 'http://4gchill.com'

# Đọc dữ liệu từ các file
proxy_file = 'proxy.txt'
ua_file = 'ua.txt'

proxies = read_proxy_file(proxy_file)
user_agents = read_user_agents_file(ua_file)

if proxies and user_agents:
    # Chọn ngẫu nhiên một proxy và một user agent
    proxy = get_random_proxy(proxies)
    user_agent = get_random_user_agent(user_agents)
    
    # Tạo session requests với proxy và user agent
    session = requests.Session()
    session.proxies = {'http': proxy, 'https': proxy}
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
else:
    print("Không có dữ liệu proxy hoặc user agent để thử nghiệm.")
