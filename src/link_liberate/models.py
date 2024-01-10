from sqlalchemy import Column, String, Integer
from .database import Base


class LiberatedLink(Base):
    __tablename__ = "liberatedlinks"
    uuid = Column(String, primary_key=True, index=True)
    link = Column(String)
