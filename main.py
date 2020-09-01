import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import json
import requests
import shutil
import slack

# spotify confing
client_secret = ""
client_id = ""
redirect_uri="http://localhost:8888"
user_name = ""

scope = 'user-read-currently-playing'

# craete access token
token = util.prompt_for_user_token( user_name,
                                    scope, 
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri
                                  )

spotify = spotipy.Spotify(auth=token)
current_track = spotify.current_user_playing_track()

artist = current_track["item"]["artists"][0]["name"]
music = current_track["item"]["name"]
thumbnails_url = current_track["item"]["album"]["images"][1]["url"]
status_emoji = ":headphones:"

listen_status = artist+' / '+music
print(listen_status)
# download thumbnails_url
r = requests.get(thumbnails_url,stream=True)
if r.status_code == 200:
    with open("thumbails.jpg", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

# slack config
client_id = ""
access_token = ""

session = requests.Session()
headers = {
        "Authorization": "Bearer %s" % access_token,
        "X-Slack-User": client_id,
        "Content-Type": "application/json; charset=utf-8"
    }

profile_set_url = 'https://slack.com/api/users.profile.set'

set_data = {
    "token" : access_token,
    "user": client_id,
    "profile":json.dumps({
        "status_text":listen_status,
        "status_emoji":status_emoji
        })
}

response = requests.post(profile_set_url,params = set_data)
# [TODO] add to errror handling
print(response)

# set thumbnails 
set_photo_url = "https://slack.com/api/users.setPhoto"
# read thumbnails.jpg
files = {
    'image': ('./thumbails.jpg', open('./thumbails.jpg', 'rb')),
    'token': (None, access_token),
}

response = requests.post(set_photo_url, files=files)
print(response)