import requests

def verify_flow():
    base_url = "http://127.0.0.1:8001/api/v1"
    
    # 1. Login
    print("Attempting login...")
    login_url = f"{base_url}/auth/login"
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        login_resp = requests.post(login_url, data=login_data)
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.status_code} - {login_resp.text}")
            return
        
        token = login_resp.json().get("access_token")
        print("Login successful, token received.")
        
        # 2. Fetch Employees
        print("Attempting to fetch employees...")
        emp_url = f"{base_url}/employees/"
        headers = {"Authorization": f"Bearer {token}"}
        
        emp_resp = requests.get(emp_url, headers=headers)
        
        if emp_resp.status_code == 200:
            print(f"Fetch employees successful. Count: {len(emp_resp.json())}")
        else:
            print(f"Fetch employees failed: {emp_resp.status_code} - {emp_resp.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    verify_flow()
