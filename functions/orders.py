import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.customers import one_customer, sub_customer_debt

from functions.users import one_user

from models.orders import Orders

from utils.pagination import pagination


def all_orders(search, status, customer_id, user, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Orders.money.like(search_formatted) | Orders.type.like(search_formatted)
    else:
        search_filter = Orders.id > 0
    if status in [True, False]:
        status_filter = Orders.status == status
    else:
        status_filter = Orders.status.in_([True, False])

    if customer_id:
        customer_id_filter = Orders.customer_id == customer_id
    else:
        customer_id_filter = Orders.customer_id > 0

    if user:
        user_filter = Orders.user_id == user.id
    else:
        user_filter = Orders.user_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    orders = db.query(Orders).options(
        joinedload(Orders.trade),joinedload(Orders.customer)).filter(Orders.date > start_date).filter(
        Orders.date <= end_date).filter(search_filter, customer_id_filter, status_filter, user_filter,
                                        ).order_by(
        Orders.id.desc())
    if page and limit:
        return pagination(orders, page, limit)

    else:
        return orders.all()


def one_order(id, db):
    return db.query(Orders).options(
        joinedload(Orders.trade),joinedload(Orders.customer)).filter(Orders.id == id).first()


async def create_order(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_customer(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    new_order_db = Orders(

        customer_id=form.customer_id,
        user_id=cur_user.id, )
    db.add(new_order_db)
    db.commit()
    db.refresh(new_order_db)

    return new_order_db


def update_order(form, cur_user, db):
    if one_order(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Orders).filter(Orders.id == form.id).update({
        Orders.customer_id: form.customer_id,
        Orders.user_id: cur_user.id,
        Orders.status: form.status
    })
    db.commit()
    return one_order(form.id, db)
