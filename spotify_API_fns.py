import spotipy
from spotipy.oauth2 import SpotifyOAuth
with open('credentials.txt') as f:
    client_id = f.readline().split('=')[1].strip()
    client_secret = f.readline().split('=')[1].strip()

client_credentials_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:3000', scope="user-library-read")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_uri(artist_name):
    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]['uri']
    else:
        return None

def get_track_uris(track_name, artist_name=None):
    if artist_name:
        results = sp.search(q='track:' + track_name + ' artist:' + artist_name, type='track')
    else:
        results = sp.search(q='track:' + track_name, type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        tracks = [item['uri'] for item in items]
        return tracks
    else:
        return None

def get_track_length_s(track_uri):
    track = sp.track(track_uri)
    return track['duration_ms']/1000

if __name__ == '__main__':
    # print(get_artist_uri('Avril Lavigne'))
    print(get_track_uris('Complicated'))
    # print(get_track_length_s('spotify:track:5xEM5hIgJ1jjgcEBfpkt2F'))