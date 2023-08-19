from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from sqlapp import crud
from sqlapp.database import SessionLocal, engine

models.base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/gardens/{g_id}', response_model=schemas.Garden)
def find_garden(g_id: int, db: Session = Depends(get_db)):
    garden_found = crud.get_garden(db, g_id=g_id)
    if garden_found is None:
        raise HTTPException(status_code=404, detail="garden not found")
    return garden_found

@app.get('/gardens/findstate', response_model=list[int])
def findstate(state:str, db: Session = Depends(get_db)):
    entry_ids = crud.get_state(db, 'assam')
    return entry_ids