from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://admin:pass@localhost/teaGarden"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
