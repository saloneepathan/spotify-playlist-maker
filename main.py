# TimeTunes: Billboard Time Capsule

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="ee1013e61fba468ba4309a876da91337",
        client_secret="c3ed136d68f14842a62196e1e6b5420e",
        show_dialog=True,
        cache_path="token.txt",
        username="Salonee Pathan",
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
song_names = [song.getText().strip() for song in soup.select("li ul li h3")]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)