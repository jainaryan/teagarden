import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

from typing import Annotated
import models, schemas
from sqlapp import crud
from sqlapp.database import SessionLocal, engine

models.base.metadata.create_all(bind=engine)

# ryj for testing
from data.fake_post import fake_posts_db

app = FastAPI()

templates = Jinja2Templates(directory="tmpl")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/blog.html', response_class=HTMLResponse)
def get_blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request,
                                                    "posts": fake_posts_db})


@app.get('/gardens/{g_id}', response_model=schemas.Garden)
def find_garden(g_id: int, db: Session = Depends(get_db)):
    garden_found = crud.get_garden(db, g_id=g_id)
    if garden_found is None:
        raise HTTPException(status_code=404, detail="garden not found")
    return garden_found


@app.get('/gardens/findstate', response_model=list[int])
def findstate(state: str, db: Session = Depends(get_db)):
    entry_ids = crud.get_state(db, 'assam')
    return entry_ids


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7000)
