from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, DateTime, func

class Base(DeclarativeBase):
    pass

class UserActivity(Base):
    __tablename__ = "user_activity"
    user_id = mapped_column(String(50), primary_key=True)
    region = mapped_column(String(5), nullable=False)
    login_counts = mapped_column(Integer, nullable=False, default=0)
    timestamp = mapped_column(DateTime, nullable=False)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())
    trace_id = mapped_column(String(50), nullable=False)

class UserMatch(Base):
    __tablename__ = "user_match"
    match_id = mapped_column(String(50), primary_key=True)
    user_id = mapped_column(String(50), nullable=False)
    kill = mapped_column(Integer, nullable=False)
    death = mapped_column(Integer, nullable=False)
    assist = mapped_column(Integer, nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
    date_created = mapped_column(DateTime, nullable=False, default=func.now())
    trace_id = mapped_column(String(50), nullable=False)
