import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.zapchast import one_zapchast,all_zapchast,create_zapchast,update_zapchast
from schemas.zapchast import *
from schemas.users import UserCurrent
router_zapchast = APIRouter()



@router_zapchast.post('/add', )
async def add_zapchast(form: ZapchastCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_zapchast(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_zapchast.get('/',  status_code = 200)
def get_zapchast(search: str = None, status: bool = True, id: int = 0, type_id:int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_zapchast(id, db)
    else :
        return all_zapchast(search=search,status=status,   page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date,user=current_user,type_id=type_id)


@router_zapchast.put("/update")
def zapchast_update(form: ZapchastUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_zapchast(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

