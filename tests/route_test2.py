import requests

BASE_URL = "http://52.205.152.205:8080"

login_data = {
    "User_mail": "allan",
    "password": "1234"
}

login_response = requests.post(f"http://52.203.72.116:8080/login", json=login_data)
if login_response.status_code != 200:
    print("Error login:", login_response.status_code, login_response.json())
    exit()

token = login_response.json()["token"]
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

graphql_query = """
query {
  following {
    User_mail
  }
}
"""

#query {
  #following {
    #Id_User
    #User_mail
  #}
#}


response = requests.post(
    f"{BASE_URL}/graphql",
    json={"query": graphql_query},
    headers=headers
)

print("\nGraphQL /following:")
print("Status:", response.status_code)
print("Response:", response.json())
