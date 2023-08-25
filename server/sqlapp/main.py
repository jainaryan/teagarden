import enum
from database import db_session
import uvicorn
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
import config
from typing import Annotated, Optional, List
import models, schemas
from sqlapp import crud
from sqlapp.crud import get_coordinates
from sqlapp.database import engine
from fastapi.middleware.cors import CORSMiddleware
from models import *
models.base.metadata.create_all(bind=engine)

# ryj for testing
from data.fake_post import fake_posts_db

app = FastAPI()
session = db_session

#templates = Jinja2Templates(directory="tmpl")
#app.mount("/static", StaticFiles(directory="static"), name="static")

#CORS PART
origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
















# Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

'''
@app.get('/blog.html', response_class=HTMLResponse)
def get_blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request,
                                                    "posts": fake_posts_db})
'''

@app.get('/gardens/{g_id}', response_model=schemas.Garden)
def find_garden(g_id: int, db: Session = Depends(get_db)):
    garden_found = crud.get_garden(db, g_id=g_id)
    if garden_found is None:
        raise HTTPException(status_code=404, detail="garden not found")
    return garden_found


@app.get('/get-all-gardens')
def get_all_gardens():
    gardens = session.query(models.Garden).all()
    return gardens


@app.get('/getcoordinates')
def get_all_coordinates():
    dictionary = {}
    coordinates = []
    gardens = session.query(models.Garden).all()
    for garden in gardens:
        coordinates.append(get_coordinates(garden))
    dictionary['coordinates'] = coordinates
    return dictionary


@app.get('/get-all-rainfalldata')
def get_all_rainfalldata():
    rainfalldata = session.query(models.RainfallData).all()
    return rainfalldata

@app.get('/gardens/findstate', response_model=list[int])
def findstate(state: str, db: Session = Depends(get_db)):
    entry_ids = crud.get_state(db, 'assam')
    return entry_ids

'''
@app.post("/add-rainfall-data")
def add_rainfall_data(entry: models.SensorData):
'''

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
