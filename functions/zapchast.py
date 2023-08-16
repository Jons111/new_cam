import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.type import one_type

from functions.users import one_user

from models.zapchast import Zapchasts

from utils.pagination import pagination


def all_zapchast(search, status, type_id, user, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Zapchasts.money.like(search_formatted) | Zapchasts.type.like(search_formatted)
    else:
        search_filter = Zapchasts.id > 0
    if status in [True, False]:
        status_filter = Zapchasts.status == status
    else:
        status_filter = Zapchasts.status.in_([True, False])

    if type_id:
        type_id_filter = Zapchasts.type_id == type_id
    else:
        type_id_filter = Zapchasts.type_id > 0

    if user:
        user_filter = Zapchasts.user_id == user.id
    else:
        user_filter = Zapchasts.user_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    zapchast = db.query(Zapchasts).options(
        joinedload(Zapchasts.type), ).filter(Zapchasts.date > start_date).filter(
        Zapchasts.date <= end_date).filter(search_filter, type_id_filter, status_filter, user_filter,
                                        ).order_by(
        Zapchasts.id.desc())
    if page and limit:
        return pagination(zapchast, page, limit)

    else:
        return zapchast.all()


def one_zapchast(id, db):
    return db.query(Zapchasts).options(
        joinedload(Zapchasts.type), ).filter(Zapchasts.id == id).first()


async def create_zapchast(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_type(form.type_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    new_zapchast_db = Zapchasts(
        name=form.name,
        birlik=form.birlik,
        size=form.size,
        number=form.number,
        type_id=form.type_id,
        user_id=cur_user.id, )
    db.add(new_zapchast_db)
    db.commit()
    db.refresh(new_zapchast_db)

    return new_zapchast_db


def update_zapchast(form, cur_user, db):
    if one_zapchast(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli zapchast mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Zapchasts).filter(Zapchasts.id == form.id).update({
        Zapchasts.type_id: form.type_id,
        Zapchasts.name: form.name,
        Zapchasts.birlik: form.birlik,
        Zapchasts.number: form.number,
        Zapchasts.size: form.size,
        Zapchasts.user_id: cur_user.id,
        Zapchasts.status: form.status
    })
    db.commit()
    return one_zapchast(form.id, db)
