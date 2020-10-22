import pandas as pd
from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
#from app.api import estimate  # , viz
from app.api import predict 




#INIT
app = FastAPI(
    title='5 best songs for you!',
    docs_url='/',
    version='0.0.0.1')

#app.include_router(estimate.router)
# app.include_router(viz.router)
app.include_router(predict.router)

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


#removing empty values from 'genre' column
#genres = genres[genres['genre'] != '']


    
    
    
   



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)