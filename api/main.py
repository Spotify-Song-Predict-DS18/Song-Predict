import pandas as pd
from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
#from app.api import estimate  # , viz

#INIT
app = FastAPI(
    title='5 best songs for you!',
    docs_url='/',
    version='0.0.0.1')

#app.include_router(estimate.router)
# app.include_router(viz.router)


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https?://.*',
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

templates = Jinja2Templates(directory="templates/")

#Description of the data we will be loading into model:
class Song:
    def __init__(self, artist, name, year, genre, duration):
        self.artist = artist
        self.name = name
        self.year = year 
        self.genre = genre
        self.duration = duration


        


#Creating some songs just to test how it works:

Rock1 = Song("Generic_band", "Crapcore", 1969, "metalcore", 3.5)
Rock2 = Song("Generic_band", "No_muffler", 2004, "heavy metal", 4)

artist_list = ['Generic_band', 'Generic_artist', 'Generic_singer']
song_list = ["Heavy Metal1", 'Glam Rock', "Jazz", "Drumnbass", "Rap", "Hell sounds"]








@app.get("/get_data")
async def get_data(_q: str = Query("Jazz", enum=song_list)):
    # _q creates a dropdown menu with a selected options. 
    #The Default option is "Jazz". The list of available options is enum=song_list
    
     #Prediction goes in here
    
    
    return {"Prediction, based on input": _q}



    
    
    
   



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)