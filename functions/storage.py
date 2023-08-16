import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.customers import one_customer 

from functions.users import one_user

from models.storage import Storage

from utils.pagination import pagination


def all_storage(search, status, zapchast_id, user, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Storage.money.like(search_formatted) | Storage.type.like(search_formatted)
    else:
        search_filter = Storage.id > 0
    if status in [True, False]:
        status_filter = Storage.status == status
    else:
        status_filter = Storage.status.in_([True, False])

    if zapchast_id:
        zapchast_id_filter = Storage.zapchast_id == zapchast_id
    else:
        zapchast_id_filter = Storage.zapchast_id > 0

    if user:
        user_filter = Storage.user_id == user.id
    else:
        user_filter = Storage.user_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    storage = db.query(Storage).options(
        joinedload(Storage.zapchast) ).filter(Storage.date >= start_date).filter(
        Storage.date <= end_date).filter(search_filter, zapchast_id_filter, status_filter, user_filter,
                                        ).order_by(
        Storage.id.desc())
    if page and limit:
        return pagination(storage, page, limit)

    else:
        return storage.all()


def one_storage(id, db):
    return db.query(Storage).options(
        joinedload(Storage.zapchast) ).filter(Storage.id == id).first()


async def create_storage(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_customer(form.zapchast_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    new_storage_db = Storage(
        name=form.name,
        birlik=form.birlik,
        size=form.size,
        number=form.number,
        zapchast_id=form.zapchast_id,
        user_id=cur_user.id, )
    db.add(new_storage_db)
    db.commit()
    db.refresh(new_storage_db)

    return new_storage_db


def update_storage(form, cur_user, db):
    if one_storage(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli storage mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Storage).filter(Storage.id == form.id).update({         
        Storage.name: form.name,
        Storage.birlik: form.birlik,
        Storage.zapchast_id: form.zapchast_id,
        Storage.size: form.size,
        Storage.price: form.price,
        Storage.number: form.number,
        Storage.currency: form.currency,
        Storage.user_id: cur_user.id,
        Storage.status: form.status
    })
    db.commit()
    return one_storage(form.id, db)
