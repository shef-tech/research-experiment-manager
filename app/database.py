from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///experiments.db"


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