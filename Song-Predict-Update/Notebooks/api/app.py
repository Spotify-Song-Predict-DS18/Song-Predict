''' 
    This file will be where most of my file will be,
    I will be using flask and creating a template for 
    my program to be displayed on a webpage.
'''

# Importing what I need 
from os import getenv
from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from .spotify import add_liked_songs, get_top_50, make_rating, add_spotify, combine
from .predict import recommend

def create_app():
    app = Flask(__name__)
    
    @app.route('/')
    def root():
        # TODO: Get a flask template and modify it to use 
        # with the current spotify model. 
        return render_template("main_page.html")
    
    @app.route('/predict')
    def song():
        sp = add_spotify()
        df1 = add_liked_songs(sp)
        df = get_top_50('37i9dQZF1DXcBWIGoYBM5M', 'spotify', sp)
        df2 = combine(df1, df)
        df2 = make_rating(df2)
        df2 = recommend(0, df2)
        return render_template('song.html', tables=[df2.to_html(classes='data')], 
                                                    titles=df2.columns.values)
    return app