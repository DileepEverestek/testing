from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR

from src.models.base_class import Base


class User(Base):
    __tablename__ ="user"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer,primary_key=True,index=True)
    username = Column(VARCHAR(100),unique=True,nullable=False)
    user_role = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100),nullable=False,unique=True,index=True)
    hashed_password = Column(VARCHAR(100),nullable=False)
