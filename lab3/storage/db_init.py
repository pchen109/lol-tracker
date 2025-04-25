from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///lol-tracker.db")

def make_session():
    return sessionmaker(bind=engine)()