from fastapi import FastAPI, Depends
from typing import Optional
import models
from database import *
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from routers.auth import get_current_user, get_user_exceptions
from routers import auth,todos, users, address
from company import companyapis, dependencies



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
app.include_router(companyapis.router, prefix="/companyapis", tags=["companyapis"], dependencies=[Depends(dependencies.get_token_header)], responses={418: {"description": "Internal use only"}})












def successful_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "deleted successfully"
    }


def http_exception():
    raise HTTPException(status_code=404, detail="Todo not found")
