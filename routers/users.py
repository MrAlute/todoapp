import sys
sys.path.append("..")

from fastapi import APIRouter, Query, Depends, HTTPException,status
import models
from database import *
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_password_hash, verify_password, get_user_exceptions

models.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"description": "user not found"}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
        
    
        
@router.get("/")
async def read_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/user/{user_id}")
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    return user

@router.get("/user")
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    return {"user": user}


@router.put("/user/password")
async def user_password_change(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    
    if user_model is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    
    if user_verification.username == user_model.username and verify_password(user_verification.password, user_model.hashed_password):
        user_model.hashed_password = get_password_hash(user_verification.new_password)
    
    db.add(user_model)
    db.commit()
    return "Successful"



@router.delete("/user/delete")
async def delete_user(user: dict= Depends(get_current_user), db: Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    
    if user_model is None:
        raise "Invalid user request"
    
    db.query(models.Users).filter(models.Users.id == user.get("id")).delete()
    
    db.commit()
    return "Delete Successful"