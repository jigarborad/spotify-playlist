from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Part 1: Authentication With Spotipy Api
scope = "playlist-modify-private"
client_id = "476d7ad4d21a4371b18558b60dce7b3c"
client_secret = "5686705251f249a89c835a68361a0ae4"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret,
                                               redirect_uri="http://example.com/", show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Get the top 100 songs from billboard website of that date
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li #title-of-a-story")
song_names = [song.getText().strip() for song in song_names_spans]
song_uri = []
year = date.split("-")[0]

# get uri of that song using spotipy api
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:  # if song is not in spotify
        print("Song doesn't exists in spotify, skipped")

# create play list
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
playlist_id = playlist["id"]

# add song to that playlist with the help of uris
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
