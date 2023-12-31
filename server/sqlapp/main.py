import os
import shutil
import zipfile

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import enum
import re
from io import StringIO
import tempfile
from pathlib import Path
from fastapi.responses import FileResponse
import pandas as pd
import jwt
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import JSON, text
from passlib.hash import bcrypt
from database import db_session
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List
import models, schemas
from schemas import *
from sqlapp import crud
from sqlapp.crud import get_coordinates, get_all_entities_with_data
from sqlapp.database import engine
from fastapi.middleware.cors import CORSMiddleware
from models import *

models.base.metadata.create_all(bind=engine)

app = FastAPI()
session = db_session

# CORS PART
origins = ['*']
JWT_SECRET = '983e5a881e16079ce4bed2ce0f4fd8f6acf0e85df658b56a41504df6fd1ea639'
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




def generate_token(user):
    user_dict = {
        "id": user.id,
        "email_id": user.email_id
    }
    token = jwt.encode(user_dict, JWT_SECRET, algorithm="HS256")
    return token



def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email_id == email).first()
    if not user or not user.verify_password(password):
        return None
    return user

# Modified login endpoint using OAuth2
@app.post("/users/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a token using JWT
    user_dict = {
        "id": user.id,
        "email_id": user.email_id,
        "role": user.authorized
    }
    access_token = jwt.encode(user_dict, JWT_SECRET, algorithm='HS256')

    return {"access_token": access_token, "token_type": "bearer"}

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
            'start_time':data.start_time.isoformat(),
            'end_time': data.end_time.isoformat(),
            #'date': data.date.isoformat(),  # Convert date to ISO format for JSON
            'entity_name': data.station.geoEntity.name,  # Add entity_name
            'entity_id': data.station.geoEntity.id,  # Add entity_id
        }
        results.append(result)

    return results


@app.get('/')
def get_entities(start_year: int, end_year: int, db: Session = Depends(get_db)):
    data = get_all_entities_with_data(db, start_year,end_year)
    return data


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = db_session.query(models.User).filter(User.email_id == payload.get('email_id')).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_400_UNAUTHORIZED,
            detail='invalid username or password')

    return schemas.User(email_id=user.email_id, name = user.name,
                        contact_number=user.contact_number, authorized=user.authorized)


@app.get('/users/details', response_model=List[UserResponse])
def get_user_details(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    for user in users:
        user_details = [{"name": user.name, "email_id": user.email_id} ]
    return user_details
@app.post('/reset-password', response_model=bool)
def reset_password(
    email_id: str,
    current_password: str,  # Change the parameter name to current_password
    new_password: str,
    user: schemas.User = Depends(get_current_user)
):
    # Check if the provided email_id matches the authenticated user's email_id
    if user.email_id != email_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email_id for the authenticated user",
        )

    # Verify the current password
    if not user.verify_password(current_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password",
        )

    # Update the user's password with the new password
    user.password = bcrypt.hash(new_password)
    db_session.commit()

    return True


@app.post('/users/create', response_model=dict)
async def create_user(user: schemas.User):
    #if check_email(user.email_id) == 0:

    user_obj = models.User(
        email_id=user.email_id,
        password=bcrypt.hash(user.password),
        name=user.name,
        contact_number=user.contact_number,
        purpose=user.purpose,
    )
    db_session.add(user_obj)
    db_session.commit()
    user_dict = {
        "email_id": user.email_id
    }
    # Generate a token for the newly registered user
    access_token = create_access_token(data=user_dict)
    return {"access_token": access_token}



'''
@app.post('/users/create', response_model=None)
def create_user(user: schemas.User):
    if (check_email(user.email_id) == 0):
        user_obj = models.User(
            email_id=user.email_id,
            password=bcrypt.hash(user.password),
            name=user.name,
            contact_number=user.contact_number,
            purpose = user.purpose,

        )
        user_obj = schemas.User
        db_session.add(user_obj)
        db_session.commit()

    elif (check_email(user.email_id) == 1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")

    elif (check_email(user.email_id) == 2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email entered")

'''
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def check_email(email_id):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (db_session.query(models.User).filter(User.email_id == email_id).first() != None):
        return 1
    else:
        if (re.fullmatch(regex, email_id)):
            return 0

        else:
            return 2


# Create an endpoint to download all data as a CSV file

@app.get("/export-data-to-csv")
def export_data_to_csv(db: Session = Depends(get_db)):
    responses = []
    temp_dir = tempfile.mkdtemp()
    exported_files = []
    tables_to_export = [
        'geoEntity',
        'station',
        'rainfallData',
        'temperatureAndHumidityInstantaneousData',
        'dailyTemperatureAndHumidityData',
        'units'
    ]

    for table_name in tables_to_export:
        # Use SQLAlchemy's text function to declare the SQL query
        query = text(f'SELECT * FROM "{table_name}"')
        # Execute the query and fetch the data
        result = db.execute(query)
        # Fetch all rows from the result set
        rows = result.fetchall()
        # Get the column names from the result set
        columns = result.keys()
        # Create a DataFrame from the rows and columns
        table_data = pd.DataFrame(rows, columns=columns)

        csv_filename = f"{table_name}.csv"
        csv_path = os.path.join(temp_dir, csv_filename)
        table_data.to_csv(csv_path, index=False)

        # Append the exported file path to the list
        exported_files.append(csv_path)

    exported_files = sorted(exported_files)
    if not exported_files:
        raise HTTPException(status_code=404, detail="No data to export")

    # Create a ZIP archive containing all the CSV files
    zip_filename = "data_export.zip"
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file_path in exported_files:
            zipf.write(file_path, os.path.basename(file_path))

    return FileResponse(zip_filename, filename=zip_filename)



    shutil.rmtree(temp_dir, ignore_errors=True)

'''
def authorize_user(email_id):
    user = db_session.query(models.User).filter(User.email_id == email_id).first()
    user.authorized = 'yes'
'''

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
