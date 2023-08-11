import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.products import one_product,all_products,create_product,update_product
from schemas.products import *
from schemas.users import UserCurrent
router_product = APIRouter()



@router_product.post('/add', )
async def add_product(form: ProductCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_product(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_product.get('/',  status_code = 200)
def get_products(search: str = None, status: bool = True, id: int = 0, type_id:int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_product(id, db)
    else :
        return all_products(search=search,status=status,   page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date,user=current_user,type_id=type_id)


@router_product.put("/update")
def product_update(form: ProductUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_product(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

