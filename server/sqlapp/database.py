from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# SQLALCHEMY_DATABASE_URL = "postgresql://admin:pass@localhost/teaGarden"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pass@localhost/postgres"

base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
conn = engine.connect()

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

def init_db():
    base.metadata.create_all(bind=engine)


