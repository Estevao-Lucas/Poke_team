from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, true
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    time = relationship("Time", back_populates="owner")


class Time(Base):
    __tablename__ = "time"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    pokemon = Column(String, index=True)
    pokemon2 = Column(String, index=True)
    pokemon3 = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", backref="times")