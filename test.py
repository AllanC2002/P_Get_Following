import requests

BASE_URL = "http://52.205.152.205:8080"

# Login
login_data = {
    "User_mail": "allan2",
    "password": "1234"
}

login_response = requests.post("http://52.203.72.116:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Error:", login_response.status_code, login_response.json())
    exit()

token = login_response.json()["token"]
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

# Get following
response = requests.get(f"{BASE_URL}/following", headers=headers)

print("\nFollowing:")
print(response.status_code)
print(response.json())
