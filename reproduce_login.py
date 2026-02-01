import requests

def test_login():
    url = "http://127.0.0.1:8001/api/v1/auth/login"
    data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    try:
        response = requests.post(url, data=data) 
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error accessing {url}: {e}")

if __name__ == "__main__":
    test_login()
