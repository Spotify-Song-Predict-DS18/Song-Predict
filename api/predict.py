
import pandas as pd
from fastapi import FastAPI, Request, Form, Query, APIRouter
import logging
import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD 
from surprise.model_selection.validation import cross_validate
from pydantic import BaseModel, Field


log = logging.getLogger(__name__)
router = APIRouter()

class User(BaseModel):
    user: int=Field(..., example=155)
    
@router.post('/predict')


def load_data():
    DATA_PATH_GENRE = 'https://raw.githubusercontent.com/Spotify-Song-Predict-DS18/Song-Predict/main/data/data_w_genres.csv'
    DATA_PATH_GENRE_2 = 'https://raw.githubusercontent.com/Spotify-Song-Predict-DS18/Song-Predict/main/data/data_by_genres.csv'
    DATA_PATH_ARTIST = 'https://raw.githubusercontent.com/Spotify-Song-Predict-DS18/Song-Predict/main/data/data_by_artist.csv'
    DATA_PATH = 'https://raw.githubusercontent.com/Spotify-Song-Predict-DS18/Song-Predict/main/data/data.csv'
    genres = pd.read_csv(DATA_PATH_GENRE)
    genre2 = pd.read_csv(DATA_PATH_GENRE_2)
    artist = pd.read_csv(DATA_PATH_ARTIST)
    control = pd.read_csv(DATA_PATH)



def clean_data():
    list_of_genres = []
    for i in genres['genres']:
        i = i[1:-1].replace("'", "")
        list_of_genres.append(i)

    genres.drop(['genres'], axis=1, inplace=True)
    genres = genres.assign(New_genres=list_of_genres)
    genres = genres.rename(columns={'New_genres':'genre', 'artists':'artist'})

    list_of_artists  = []
    for k in control['artists']:
        k = k[1:-1].replace("'", "")
        list_of_artists.append(k)
    list_of_artists = []   
    control.drop(['artists'], axis=1, inplace=True)
    control = control.assign(New_artists=list_of_artists)
    control = control.rename(columns={'New_artists':'artist'})


def preprocessing():
    result = pd.merge(control, genres[['artist', 'genre']], how='left', on='artist')
    result = result[result['genre'].isnull() == False]
    result['release_date'] = pd.to_datetime(control['release_date'])
    result['user'] = np.random.randint(0, 200, result.shape[0])

def model_training():
    reader = Reader(rating_scale=(0,100))
    data = Dataset.load_from_df(result[['user', 'id', 'popularity']],
                           reader)

    svd = SVD()
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5,
              verbose=True)
    trainset = data.build_full_trainset()
    svd.fit(trainset)

#Running functions
load_data()
clean_data()
preprocessing()
model_training()


     
def recommend(userid, df):
    '''A function that will take a userid and predict music based their listen history
    With this database, will only take ids ranging 0-200.
    
    Returns a new column called "Estimate Score" which represents the chance that the
    use will like the music
    
    Score will not be high on average, since users are randomly generated.'''
    
    # First passing through a if statment to make sure 
    # The ID matches the requirements. 
    if userid > 200:
        return "ERROR: User ID too high, must be between 0-200"
    elif userid < 0:
        return "ERROR: User ID too low, must be between 0-200"
    else:
        print("Generating music recommendation...")
    
    # Intantiating my reader and my data
    reader = Reader(rating_scale=(0,100))
    data = Dataset.load_from_df(result[['user', 'id', 'popularity']],
                            reader)
    # Intatntiating my SVD 
    svd = SVD()
    
    # Running a 5-fold cross-validation 
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5,
                    verbose=True)
    
    # Retraining the model using the entire dataset
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    
    # Model has been trained, time to use for prediction.
    titles = result.copy()

    titles['Estimate_Score'] = titles['id'].apply(lambda x: svd.predict(userid, x).est)
    
    # Creating a mask that does not include songs the user already has. 
    mask = titles['user'] != userid
    titles = titles[mask]
    
    # Now returning the top 5 songs for that user.
    titles = titles.sort_values(by=['Estimate_Score'], ascending=False)
    
    titles = titles.head(5)
    
    titles = [titles.columns.values.tolist()] + titles.values.tolist()
    return titles