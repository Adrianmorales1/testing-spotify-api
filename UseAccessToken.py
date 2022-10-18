import datetime
import base64
import requests
from urllib.parse import urlencode

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_credentials(self):
        """
        returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("you must set client id and client secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
                    "Authorization" : f"Basic {client_creds_b64}"
                }
    
    def get_token_data(self):
        return {
                 "grant_type" : "client_credentials"
            }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_headers()
        r  = requests.post(token_url, data=token_data,headers=token_header)
        print(r.json())
        valid_request = r.status_code not in range(200,299)
        if valid_request:
            return False
        print("It is valid!!")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

client_id = "310c337f3b7247a49d84b12c5c1de6ba"
client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"

spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
print(spotify.access_token)
access_token = spotify.access_token
headers = {
    "Authorization" : f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({'q' : 'Tadow', "type" : "track"})
print(data)
lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
print(r.status_code)
print(r.json())