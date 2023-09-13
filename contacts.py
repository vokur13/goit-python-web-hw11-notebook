from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.Contact)
async def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = await crud.get_contact_by_email(db, email=contact.email)
    if db_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return await crud.create_contact(db=db, contact=contact)


@router.get("/", response_model=List[schemas.Contact])
async def read_contacts(
    skip: int = 0, limit: int = Query(10, le=100), db: Session = Depends(get_db)
):
    contacts = await crud.get_contacts(db, skip=skip, limit=limit)
    return contacts


@router.get("/{contact_id}", response_model=schemas.Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.Contact)
async def update_contact(
    contact: schemas.ContactCreate, contact_id: int, db: Session = Depends(get_db)
):
    db_contact = await crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return await crud.update_contact(db_contact, contact, db)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return await crud.remove_contact(db_contact, db)
