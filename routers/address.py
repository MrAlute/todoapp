import sys
sys.path.append("..")

from fastapi import APIRouter, Depends
from typing import Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exceptions


router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {"description": "Not foound"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
        
        
class Address(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[int]
    
    
@router.post("/")
async def create_address_detail(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    
    address_modal = models.Address()
    address_modal.address1 = address.address1
    address_modal.address2 = address.address2
    address_modal.city = address.city
    address_modal.state = address.state
    address_modal.country = address.country
    address_modal.postalcode = address.postalcode
    address_modal.apt_num = address.apt_num
    
    db.add(address_modal)
    db.flush()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    
    user_model.address_id = address_modal.id
    db.add(user_model)
    db.commit()