from sqlalchemy import (
    Column, Integer, Float, String, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    body_weight_kg = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    exercises = relationship("Exercise", back_populates="log_entry", cascade="all, delete-orphan")
    foods = relationship("Food", back_populates="log_entry", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    log_entry_id = Column(Integer, ForeignKey("log_entries.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    time_min = Column(Float, nullable=True)

    log_entry = relationship("LogEntry", back_populates="exercises")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    log_entry_id = Column(Integer, ForeignKey("log_entries.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    quantity_g = Column(Float, nullable=True)
    quantity_items = Column(Integer, nullable=True)

    log_entry = relationship("LogEntry", back_populates="foods")
