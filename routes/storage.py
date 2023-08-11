import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.storage import one_storage,all_storage,create_storage,update_storage
from schemas.storage import *
from schemas.users import UserCurrent
router_storage = APIRouter()



@router_storage.post('/add', )
async def add_storage(form: StorageCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_storage(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_storage.get('/',  status_code = 200)
def get_storage(search: str = None, status: bool = True, id: int = 0, zapchast_id:int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_storage(id, db)
    else :
        return all_storage(search=search,status=status,   page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date,user=current_user,zapchast_id=zapchast_id)


@router_storage.put("/update")
def storage_update(form: StorageUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_storage(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

