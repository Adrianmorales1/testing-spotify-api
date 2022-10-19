import datetime
import base64
from this import d
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
            raise Exception("Could not authenticate client.")
            
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

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type ='albums', version = 'v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
        pass

    def get_album(self,_id):
        return self.get_resource(_id, resource_type = 'albums', version='v1')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type = 'artists', version='v1')

    def get_track(self, _id):
        return self.get_resource(_id, resource_type = 'tracks', version='v1')

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        print(r.status_code)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    def search(self, query = None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query,dict):
            query == ""
        query_params = urlencode({'q' : query, "type" : search_type.lower()})
        return self.base_search(query_params)


client_id = "310c337f3b7247a49d84b12c5c1de6ba"
client_secret = "2d36f1dd9ed54c6f99af70d48e7495bf"

spotify = SpotifyAPI(client_id, client_secret)
#print(spotify.search('Tadow','track')['tracks']['items'][0]['id']) #SPOTIFY TRACK ID
#print(spotify.search('Tadow','track')['tracks']['items'][0]['name'])  #TRACK TITLE
#print(spotify.search('Tadow','track')['tracks']['items'][0]['album']['artists'][0]['name'])#ARTIST NAME
#print(spotify.search('Tadow','track')['tracks']['items'][0]['album']['artists'][0]['external_urls']) #ARTIST URL TO THEIR PAGE ON SPOTIFY
#print(spotify.search('Tadow','track')['tracks']['items'][0]['album']['images'][-1]['url']) #IMAGE OF TRACK

#track_list = spotify.search('Over you','track')['tracks']['items']
#count = 0
#track_id_trial = None
#for track in track_list:
#   if count == 0:
#        track_id_trial = track['id']
#        print("---------- FIRST TRACK DOWN BELOW ----------")
#        count = 1
#    print("title: " + track['name'] + ", artist: " + track['album']['artists'][0]['name'])
#    print("SPOTIFY ALBUM ID: " + track['id'])
#    print("IMAGE OF TRACK: ")
#    url_album_cover = track['album']['images'][-2]['url']
#    print(url_album_cover)
#print(spotify.get_artist("3ycxRkcZ67ALN3GQJ57Vig")["name"])
#trial_id = spotify.get_track(track_id_trial)
#print("------ First Track in file ------")
#print("title: " + trial_id['name'] + ", artist: " + trial_id['album']['artists'][0]['name'])
#print("SPOTIFY ALBUM ID: " + trial_id['id'])
#print("IMAGE OF TRACK: ")
#url_album_cover = trial_id['album']['images'][-2]['url']
#print(url_album_cover)

def search_query(query):
    track_list = spotify.search(query,'track')['tracks']['items']
    track_list_file = []
    for track in track_list:
        track_list_file.append({
            'title' : track['name'],
            'artist' : track['album']['artists'][0]['name'],
            'id' : track['id'],
            'image_url' : track['album']['images'][-2]['url']
        })
    return track_list_file

track_list = search_query("Tadow")
for track in track_list:
    print("title: " + track['title'] + ", artist: " + track['artist'])
    print("SPOTIFY ALBUM ID: " + track['id'])
    print("IMAGE OF TRACK: ")
    url_album_cover = track['image_url']
    print(url_album_cover)
