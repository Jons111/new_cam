import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload


from functions.users import one_user
from models.trade import Trades

from utils.pagination import pagination


def all_trades(search, status,order_id,   start_date, end_date,user, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Trades.name.like(search_formatted)
    else:
        search_filter = Trades.id > 0
    if status in [True, False]:
        status_filter = Trades.status == status
    else:
        status_filter = Trades.status.in_([True, False])

    if order_id:
        trade_id_filter = Trades.order_id == order_id
    else:
        trade_id_filter = Trades.id > 0

    if user:
        user_filter = Trades.user_id == user.id
    else:
        user_filter = Trades.id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    trades = db.query(Trades).filter(Trades.date > start_date).filter(
        Trades.date <= end_date).filter(search_filter, status_filter,trade_id_filter,user_filter  ).order_by(
        Trades.id.desc())
    if page and limit:
        return pagination(trades, page, limit)

    else:
        return trades.all()


def one_trade(id, db):
    return db.query(Trades).filter(Trades.id == id).first()


async def create_trade(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")



    new_trade_db = Trades(
        zapchast_id=form.zapchast_id,
        quantity=form.quantity,
        order_id=form.order_id,
        user_id=cur_user.id,

    )
    db.add(new_trade_db)
    db.commit()
    db.refresh(new_trade_db)

    return new_trade_db


def update_trade(form, cur_user, db):
    if one_trade(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli trade mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Trades).filter(Trades.id == form.id).update({
        Trades.zapchast_id: form.zapchast_id,
        Trades.quantity: form.quantity,
        Trades.order_id: form.order_id,
        Trades.user_id: cur_user.id,
        Trades.status: form.status
    })
    db.commit()
    return one_trade(form.id, db)
