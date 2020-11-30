''' 
    Takes my table model and mixes them with the spotify API to grab data.
''' 
# Importing what I need 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd 

# TODO: Create Evoiroment variables for the ids... 
CLIENT_ID = '305996eeec9c42cb807aebcd48a82b29'
ID = '3699864be2834ad695827d8092e91812'
REDIRECT_URI = 'http://example.com'

def add_spotify():
    SPOTIPY_CLIENT_ID = '305996eeec9c42cb807aebcd48a82b29'
    SPOTIPY_SECRET_ID = '3699864be2834ad695827d8092e91812'
    SPOTIPY_REDIRECT_URI = 'http://example.com'

    scope = 'user-library-read'
    # authorizing the use of my liked songs list 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
                                               client_secret=SPOTIPY_SECRET_ID, 
                                               client_id=SPOTIPY_CLIENT_ID, 
                                               redirect_uri=SPOTIPY_REDIRECT_URI))

    return sp
# adding the liked songs to the model. 
def add_liked_songs(sp):
    # creating an empty DataFrame
    song_feature_list = ['artist', 'album', 'track_name', 'track_id', 'popularity',
                        'danceability', 'energy', 'key', 'loudness',
                        'mode', 'speechiness', 'instrumentalness',
                        'liveness', 'valence', 'tempo', 'duration_ms',
                        'time_signature']
    
    song_df = pd.DataFrame(columns = song_feature_list)
    
    # Now we got to loop through every track in the liked songs list, extract
    # features and append the features to the liked songs df 
    
    i = 0
    offset = 0
    # for speeds sake will be keeping the loop to only have 400 iterations.
    while i < 400:
        liked_songs = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        for track in liked_songs:
            # create an empty dict
            song_features = {}

            # getting metadata
            song_features["artist"] = track["track"]["album"]["artists"][0]['name']
            song_features["album"] = track['track']['album']['name']
            song_features["track_name"] = track['track']['name']
            song_features['track_id'] = track['track']['id']
            song_features['popularity'] = track["track"]['popularity']

            # Getting audio features
            audio_features = sp.audio_features(song_features['track_id'])[0]
            for feature in song_feature_list[5:]:
                song_features[feature] = audio_features[feature]

            track_df = pd.DataFrame(song_features, index = [0])
            song_df = pd.concat([song_df, track_df], ignore_index=True)
        i += 1
        offset += 50
    return song_df

# Now making the get top 50, which would get the top 50 songs
# From the top 50 playlist

def get_top_50(playlist_id, creator, sp):
    # Creating an empty DataFrame
    # Create empty dataframe
    playlist_features_list = ["artist", "album", "track_name", "track_id", 'popularity', 
                             "danceability", "energy", "key", "loudness", "mode", "speechiness",
                             "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Create empty dict
    playlist_features = {}
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        playlist_features['popularity'] = track["track"]['popularity']
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[5:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

    # My third funtion that will create the rating of the dataset. 

def make_rating(df):
    #
    #a function that will take in the audio values 
    #and returns a total 'rating' which is a score 
    #that is an average of all the audio values to 
    #an easy number for the model. 
    
    total = [df['popularity'], df['danceability'], df['energy'], df['key'],
            df['loudness'], df['mode'], df['speechiness'], df['instrumentalness'],
            df['liveness'], df['valence'], df['tempo'], df['duration_ms']]
    
    df['rating'] = sum(total) / 12
    
    #divides the numbers by 1000 so it returns a number that is 0-50
    df['rating'] = df['rating'] / 1000
    
    return df

def combine(playlist, liked_song):
    # Setting up the "user id" 
    # This will be run with the model to find which songs are liked and which songs 
    # are from the top playlist... 
    playlist['user'] = 0
    liked_song['user'] = 1
    # Concating the dataframes. 
    full_song = pd.concat([playlist, liked_song], ignore_index=True)
    return full_song