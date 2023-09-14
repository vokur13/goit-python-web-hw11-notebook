from sqlalchemy import Column, Integer, String, DateTime, func


from src.db.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True, unique=True, index=True)
    birth_date = Column(DateTime, nullable=True)
    bio = Column(String, nullable=True)
    created_at = Column("created_at", DateTime, default=func.now())
