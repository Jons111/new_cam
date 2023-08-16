import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.type import one_type

from functions.users import one_user

from models.products import Products

from utils.pagination import pagination


def all_products(search, status, type_id, user, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Products.money.like(search_formatted) | Products.type.like(search_formatted)
    else:
        search_filter = Products.id > 0
    if status in [True, False]:
        status_filter = Products.status == status
    else:
        status_filter = Products.status.in_([True, False])

    if type_id:
        type_id_filter = Products.type_id == type_id
    else:
        type_id_filter = Products.type_id > 0

    if user:
        user_filter = Products.user_id == user.id
    else:
        user_filter = Products.user_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    products = db.query(Products).options(
        joinedload(Products.type)).filter(Products.date >= start_date).filter(
        Products.date <= end_date).filter(search_filter, type_id_filter, status_filter, user_filter,
                                        ).order_by(
        Products.id.desc())
    if page and limit:
        return pagination(products, page, limit)

    else:
        return products.all()


def one_product(id, db):
    return db.query(Products).options(
        joinedload(Products.type)).filter(Products.id == id).first()


async def create_product(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_type(form.type_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    new_product_db = Products(
        name=form.name,
        type_id=form.type_id,
        price=form.price,
        currency=form.currency,
        user_id=cur_user.id, )
    db.add(new_product_db)
    db.commit()
    db.refresh(new_product_db)

    return new_product_db


def update_product(form, cur_user, db):
    if one_product(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli product mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Products).filter(Products.id == form.id).update({         
        Products.name: form.name,
        Products.type: form.type,
        Products.price: form.price,
        Products.currency: form.currency,
        Products.user_id: cur_user.id,
        Products.status: form.status
    })
    db.commit()
    return one_product(form.id, db)
