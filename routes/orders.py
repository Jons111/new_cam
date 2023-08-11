import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.orders import one_order,all_orders,create_order,update_order
from schemas.orders import *
from schemas.users import UserCurrent
router_order = APIRouter()



@router_order.post('/add', )
async def add_order(form: OrderCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_order(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_order.get('/',  status_code = 200)
def get_orders(search: str = None, status: bool = True, id: int = 0, customer_id:int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_order(id, db)
    else :
        return all_orders(search=search,status=status,   page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date,user=current_user,customer_id=customer_id)


@router_order.put("/update")
def order_update(form: OrderUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_order(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

