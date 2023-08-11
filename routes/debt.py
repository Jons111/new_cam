from fastapi import APIRouter, Depends, HTTPException
from pydantic.datetime_parse import date
import datetime
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.debts import one_debt, all_debts, create_debt, update_debt, debt_result
from schemas.debts import DebtCreate, DebtUpdate
from schemas.users import UserCurrent

router_debt = APIRouter()


@router_debt.post('/add')
def add_debt(form: DebtCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user
    if create_debt(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_debt.get('/', status_code=200)
def get_debts(search: str = None, status: bool = True,debt_status: bool = True, id: int = 0, customer_id: int = 0, page: int = 1,
               limit: int = 25,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_debt(id, db)
    else:
        return all_debts(search=search, status=status,debt_status=debt_status, page=page, limit=limit, db=db, customer_id=customer_id,user=current_user)


@router_debt.put("/update")
def debt_update(form: DebtUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if update_debt(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


# @router_debt.get('/result', status_code=200)
# def get_lifetimes(start_date: date = datetime.datetime.now().date().min,
#                   end_date: date = datetime.datetime.now().date().max,
#                   db: Session = Depends(get_db),
#                   current_user: UserCurrent = Depends(
#                       get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
#      return debt_result(user=current_user,start_date=start_date,end_date=end_date,db=db)
#
