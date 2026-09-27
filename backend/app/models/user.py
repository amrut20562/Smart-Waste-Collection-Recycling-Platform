from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from app.db import Base
import enum

class UserRole(str, enum.Enum):
    CITIZEN = "CITIZEN"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())