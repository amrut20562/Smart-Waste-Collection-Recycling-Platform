from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db import Base

class WasteCategory(Base):
    __tablename__ = "waste_categories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    waste_stream = Column(String, nullable=False)
    instructions = Column(Text, nullable=False)
    special_handling = Column(Boolean, default=False)
    pickup_supported = Column(Boolean, default=True)
    warning = Column(String, nullable=True)