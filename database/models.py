from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)
from sqlalchemy.orm import (
    declarative_base,
)
from datetime import datetime

Base = declarative_base()

class User(Base):


    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    is_paid = Column(Boolean, default=False)
    access_token = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    label = Column(String, nullable=True)
    label_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
