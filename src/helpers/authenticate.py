# Logic for handling spotify authentication
import spotipy


def spotify_authenticate():
    #If you want to use your own Spotify application change client_id here.
    client_id = "2a487b56eba34dbdb32c7109f6292b9c"
    redirect_uri = "http://127.0.0.1:8080"
    auth_manager = spotipy.oauth2.SpotifyPKCE(scope='user-read-currently-playing', client_id = client_id,
                                               redirect_uri = redirect_uri, cache_path = 'src/helpers/.cache/.spotcache')
    spotify_token = spotipy.Spotify(auth_manager.get_access_token())
    return spotify_token