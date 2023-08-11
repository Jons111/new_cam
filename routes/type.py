import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.type import one_type,all_types,create_type,update_type
from schemas.type import *
from schemas.users import UserCurrent
router_type = APIRouter()



@router_type.post('/add', )
async def add_type(form: TypeCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_type(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_type.get('/',  status_code = 200)
def get_types(search: str = None, status: bool = True, id: int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.utcnow().date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_type(id, db)
    else :
        return all_types(search=search,status=status,  page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_type.put("/update")
def type_update(form: TypeUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_type(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

