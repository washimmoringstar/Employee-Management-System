import asyncio
import httpx
import sys

async def verify():
    base_url = "http://127.0.0.1:8003"
    async with httpx.AsyncClient(base_url=base_url) as client:
        print("1. Logging in as Admin...")
        response = await client.post("/api/v1/auth/login", data={"username": "admin@example.com", "password": "admin123"})
        if response.status_code != 200:
            print(f"Admin login failed: {response.text}")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   Admin logged in.")

        print("2. Listing Users (Expect success)...")
        response = await client.get("/api/v1/users/", headers=headers)
        if response.status_code != 200:
            print(f"   Failed to list users: {response.text}")
        else:
            print(f"   Success. Users found: {len(response.json())}")

        print("3. Creating a new User...")
        new_user = {
            "email": "newuser@example.com",
            "password": "password123",
            "role": "staff"
        }
        response = await client.post("/api/v1/users/", json=new_user, headers=headers)
        if response.status_code != 200:
            print(f"   Failed to create user: {response.text}")
            return
        
        user_data = response.json()
        user_id = user_data["id"]
        print(f"   User created: ID {user_id}, Email {user_data['email']}")

        print("4. Updating the User...")
        update_data = {"role": "hr"}
        response = await client.put(f"/api/v1/users/{user_id}", json=update_data, headers=headers)
        if response.status_code != 200:
            print(f"   Failed to update user: {response.text}")
        else:
            print(f"   User updated. New role: {response.json()['role']}")

        print("5. Deleting the User...")
        response = await client.delete(f"/api/v1/users/{user_id}", headers=headers)
        if response.status_code != 200:
            print(f"   Failed to delete user: {response.text}")
        else:
             print("   User deleted successfully.")

        print("6. Verifying Deletion...")
        response = await client.get(f"/api/v1/users/{user_id}", headers=headers)
        if response.status_code == 404:
            print("   Confimed: User not found.")
        else:
            print(f"   Error: User still exists or other error: {response.status_code}")

if __name__ == "__main__":
    try:
        asyncio.run(verify())
    except Exception as e:
        print(f"Verification failed: {e}")
