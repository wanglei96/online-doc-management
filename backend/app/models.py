from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)  # 指定长度为255
    hashed_password = Column(String(255))  # 指定长度为255
    is_admin = Column(Integer, default=0)  # 0 for read-only, 1 for admin

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)  # 指定长度为255
    upload_time = Column(DateTime, default=datetime.datetime.now)
    uploader_id = Column(Integer, ForeignKey("users.id"))

    uploader = relationship("User")