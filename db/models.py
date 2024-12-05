from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from database import Base
from app.main import Categories

class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    comment_message = Column(String, index=True)
    comment_name = Column(String, index=True)
    comment_category = Column(Enum(Categories), index=True)

