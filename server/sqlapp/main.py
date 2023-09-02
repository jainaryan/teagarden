import enum
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import JSON
from passlib.hash import bcrypt
from database import db_session
import uvicorn
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, Header, status
from sqlalchemy.orm import Session
import config
from typing import Annotated, Optional, List
import models, schemas
from sqlapp import crud
from sqlapp.crud import get_coordinates, get_all_entities_with_data
from sqlapp.database import engine
from fastapi.middleware.cors import CORSMiddleware
from models import User
models.base.metadata.create_all(bind=engine)
# ryj for testing
from data.fake_post import fake_posts_db
app = FastAPI()
session = db_session
# templates = Jinja2Templates(directory="tmpl")
# app.mount("/static", StaticFiles(directory="static"), name="static")
# CORS PART
origins = ['https://localhost:3000']
JWT_SECRET ='4ded425af3e0b0da6284b8f860cfae26'
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
'''
@app.get('/blog.html', response_class=HTMLResponse)
def get_blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request,
                                                    "posts": fake_posts_db})
'''
#def get_current_user(token: str = Depends(oauth2_scheme)):
@app.get('/gardens/{g_id}', response_model=schemas.GeoEntity)
def find_garden(g_id: int, db: Session = Depends(get_db)):
    garden_found = crud.get_entity(db, g_id=g_id)
    if garden_found is None:
        raise HTTPException(status_code=404, detail="entity not found")
    return garden_found
@app.get('/get-all-gardens', response_model=List[schemas.GeoEntityBase])
def get_all_gardens():
    entities = session.query(models.GeoEntity).all()
    return entities
@app.get('/get-all-rainfalldata')
def get_all_rainfalldata():
    # Join RainfallData with Station and then Station with GeoEntity
    rainfalldata = (
        session.query(models.RainfallData)
        .join(models.Station)
        .join(models.GeoEntity)
        .all()
    )

    # Create a list to hold the results with entity_name and entity_id
    results = []

    # Iterate through the RainfallData objects and extract entity_name and entity_id
    for data in rainfalldata:
        result = {
            'id': data.id,
            'station_id': data.station_id,
            'reading': data.reading,
            'date': data.date.isoformat(),  # Convert date to ISO format for JSON
            'entity_name': data.station.geoEntity.name,  # Add entity_name
            'entity_id': data.station.geoEntity.id,  # Add entity_id
        }
        results.append(result)

    return results


@app.get('/')
def get_entities(year: int, db: Session = Depends(get_db)):
    data = get_all_entities_with_data(db, year)
    return data[0]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')
def authenticate_user(emailid: str, password: str):
    user = db_session.query(models.User).filter(User.email_id==emailid).first()
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = db_session.query(models.User).filter(User.email_id==payload.get('email_id')).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid username or password')

    return schemas.User(email_id = user.email_id, first_name = user.first_name, last_name = user.last_name, contact_number= user.contact_number, purpose = user.purpose.value)

@app.get('/users/me', response_model=schemas.User)
def get_user(user: schemas.User = Depends(get_current_user)):
    return user

@app.post('/users', response_model=None)
def create_user(user: schemas.User):
    user_obj = models.User(email_id= user.email_id, password = bcrypt.hash(user.password), first_name = user.first_name, last_name = user.last_name, contact_number = user.contact_number, id = user.id, purpose = user.purpose.value)
    db_session.add(user_obj)
    db_session.commit()


@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return {"error": "invalid credentials"}
    user_dict = {
        "id": user.id,
        "password": user.password,
        "email_id": user.email_id,

    }

    token = jwt.encode(user_dict, JWT_SECRET, algorithm="HS256")
    return {'access_token': token, 'token_type': 'bearer'}
'''
@app.post("/add-rainfall-data")
def add_rainfall_data(entry: models.SensorData):
'''
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)