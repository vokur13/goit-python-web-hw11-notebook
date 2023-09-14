from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy.orm import Session


from src.db import models
from src.schemas.contacts import ContactCreate


async def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


async def get_contact_by_email(db: Session, email: EmailStr):
    return db.query(models.Contact).filter(models.Contact.email == email).first()


async def get_contacts(
    db: Session,
    email: str | None,
    first_name: str | None,
    last_name: str | None,
    skip: int,
    limit: int,
):
    contacts = db.query(models.Contact)

    if email:
        contacts = contacts.filter(models.Contact.email.ilike(f"%{email}%"))
    elif first_name:
        contacts = contacts.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    elif last_name:
        contacts = contacts.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    contacts = contacts.offset(skip).limit(limit).all()
    return contacts


async def read_contacts_by_week_to_birthday(
    db: Session,
    skip: int,
    limit: int,
):
    contacts = db.query(models.Contact)

    current_datetime = datetime.now().date()
    delta = timedelta(days=7)
    future_datetime = current_datetime + delta

    bd_list = list()
    for contact in contacts:
        bd = datetime(
            year=current_datetime.year,
            month=contact.birth_date.month,
            day=contact.birth_date.day,
        ).date()
        if (future_datetime - bd) <= delta:
            bd_list.append(contact)

    return bd_list


async def create_contact(contact: ContactCreate, db: Session):
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
    db_contact, contact: ContactCreate, db: Session
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
