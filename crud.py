from pydantic import EmailStr
from sqlalchemy.orm import Session

import models, schemas


async def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


async def get_contact_by_email(db: Session, email: EmailStr):
    return db.query(models.Contact).filter(models.Contact.email == email).first()


async def get_contacts(db: Session, skip: int, limit: int):
    return db.query(models.Contact).offset(skip).limit(limit).all()


async def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birth_date=contact.birth_date,
        bio=contact.bio,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def update_contact(
    db_contact, contact: schemas.ContactCreate, db: Session
) -> models.Contact | None:
    db_contact.first_name = contact.first_name
    db_contact.last_name = contact.last_name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    db_contact.birth_date = contact.birth_date
    db_contact.bio = contact.bio
    db.commit()
    return db_contact


async def remove_contact(db_contact, db: Session):
    db.delete(db_contact)
    db.commit()
