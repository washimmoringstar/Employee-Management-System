import asyncio
import httpx
import sys

async def verify():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        print("Checking health...")
        # Since we don't have a health check, we'll just check if /docs loads (status 200)
        response = await client.get("/docs")
        print(f"Docs status: {response.status_code}")
        
        if response.status_code != 200:
            print("Failed to access /docs")
            return

        print("Testing Signup...")
        email = "test@example.com"
        password = "strongpassword"
        response = await client.post("/api/v1/auth/signup", json={"email": email, "password": password})
        print(f"Signup status: {response.status_code}")
        if response.status_code not in [200, 400]: # 400 if already exists
             print(f"Signup failed: {response.text}")
        
        print("Testing Login...")
        response = await client.post("/api/v1/auth/login", data={"username": email, "password": password})
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Got token")
            
            print("Testing Create Employee...")
            headers = {"Authorization": f"Bearer {token}"}
            emp_data = {"name": "Test Emp", "email": "emp@test.com", "position": "Dev", "salary": 50000}
            response = await client.post("/employees/", json=emp_data, headers=headers)
            print(f"Create Employee status: {response.status_code}")
            # Note: Create employee might fail if user role is not admin/hr, which default is staff.
            # But the endpoint uses require_hr_or_admin. 
            # Default user created is 'staff'. So this should return 403.
            if response.status_code == 403:
                print("Correctly denied access to staff user.")

if __name__ == "__main__":
    try:
        asyncio.run(verify())
    except Exception as e:
        print(f"Verification failed: {e}")
