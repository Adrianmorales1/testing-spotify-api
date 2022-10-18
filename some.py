import base64
import requests
import datetime

client_id = "310c337f3b7247a49d84b12c5c1de6ba"
client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"

client_creds = f"{client_id}:{client_secret}"

client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type" : "client_credentials"
}
token_header = {
    "Authorization" : f"Basic {client_creds_b64.decode()}"
}

r  = requests.post(token_url, data=token_data,headers=token_header)
print(r.json())
valid_request = r.status_code in range(200,299)
if valid_request:
    print("It is valid!!")
    token_response_data = r.json()
    now = datetime.datetime.now()
    access_token = token_response_data['access_token']
    expires_in = token_response_data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now