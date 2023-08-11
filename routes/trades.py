import datetime

from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.trades import one_trade,all_trades,create_trade,update_trade
from schemas.trades import *
from schemas.users import UserCurrent
router_trade = APIRouter()



@router_trade.post('/add', )
async def add_trade(form: TradeCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_trade(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_trade.get('/',  status_code = 200)
def get_trades(search: str = None, status: bool = True, id: int = 0, order_id:int = 0,  start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_trade(id, db)
    else :
        return all_trades(search=search,status=status,   page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date,user=current_user,order_id=order_id)


@router_trade.put("/update")
def trade_update(form: TradeUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_trade(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")

