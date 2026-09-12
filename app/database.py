import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()


def build_database_url():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if all([
        db_host,
        db_port,
        db_name,
        db_user,
        db_password
    ]):
        return URL.create(
            "postgresql+psycopg",
            username=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port),
            database=db_name
        )

    return "sqlite:///experiments.db"


DATABASE_URL = build_database_url()


engine = create_engine(
    DATABASE_URL,
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def init_db():
    from app.models import Experiment

    Base.metadata.create_all(
        bind=engine
    )