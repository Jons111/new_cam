from fastapi import APIRouter, Depends, HTTPException
from pydantic.datetime_parse import date

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user
import  datetime
Base.metadata.create_all(bind=engine)

from functions.black_list import one_black_list, create_black_list, update_black_list, all_black_lists, black_list_delete
from schemas.black_list import *
from schemas.users import *

router_black_list = APIRouter()


@router_black_list.post('/add', )
def add_black_list(form: Black_ListCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    if create_black_list(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_black_list.get('/', status_code=200)
def get_black_lists(search: str = None, status: bool = True, id: int = 0,trade_id: int = 0,
                    customer_id:int=0,
                    start_date: date = datetime.datetime.now().date().min,
                    end_date: date = datetime.datetime.now().date().today(),
                    deadline: date = None,
                  page: int = 1,
                  limit: int = 25, db: Session = Depends(get_db),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    if id:
        return one_black_list(id, db)

    else:
        return all_black_lists(search=search,
                               status=search,
                               trade_id=trade_id,
                               customer_id=customer_id,
                               start_date=start_date,
                               end_date=end_date,
                               page=page,
                               limit=limit,
                               db=db,
                               deadline=deadline)


@router_black_list.put("/update")
def black_list_update(form: Black_ListUpdate, db: Session = Depends(get_db),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    if update_black_list(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_black_list.delete('/{id}', status_code=200)
def delete_black_list(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    if id:
        return black_list_delete(id,  db)
