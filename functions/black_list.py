from fastapi import HTTPException
import datetime

from sqlalchemy.orm import joinedload

from functions.customers import one_customer
from functions  import debts
from functions.users import one_user
from models.black_list import Black_list
from models.customers import Customers
from models.users import Users

from utils.pagination import pagination


def all_black_lists(search, status, trade_id, customer_id, start_date, end_date, deadline, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Black_list.money.like(search_formatted)
    else:
        search_filter = Black_list.id > 0
    if status in [True, False]:
        status_filter = Black_list.status == status
    else:
        status_filter = Black_list.status.in_([True, False])

    if trade_id:
        trade_id_filter = Black_list.trade_id == trade_id
    else:
        trade_id_filter = Black_list.id > 0

    if customer_id:
        customer_id_filter = Black_list.customer_id == customer_id
    else:
        customer_id_filter = Black_list.id > 0

    if deadline:
        deadline_filter = Black_list.deadline == deadline
    else:
        deadline_filter = Black_list.id > 0

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    black_lists = db.query(Black_list).options(joinedload(Black_list.customer)).filter(
        Black_list.date > start_date).filter(
        Black_list.date <= end_date).filter(search_filter, deadline_filter, status_filter, trade_id_filter,
                                            customer_id_filter).order_by(Black_list.id.desc())
    if page and limit:
        return pagination(black_lists, page, limit)
    else:
        return black_lists.all()


def one_black_list(id, db):
    return db.query(Black_list).options(Black_list.customer).joinedload(Customers).filter(Black_list.id == id).first()


def check_black_list(customer_id, db):
    return db.query(Black_list).filter(Black_list.customer_id == customer_id).first()


def create_black_list(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_customer(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    if debts.one_debt(form.trade_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    new_black_list_db = Black_list(
        money=form.money,
        trade_id=form.trade_id,
        customer_id=form.customer_id,
        user_id=cur_user.id,
    )
    db.add(new_black_list_db)
    db.commit()
    db.refresh(new_black_list_db)
    return new_black_list_db


def add_black_list(money, trade_id, customer_id, deadline, cur_user_id, db):
    if one_user(cur_user_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_customer(customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    if debts.one_debt(trade_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    new_black_list_db = Black_list(
        money=money,
        trade_id=trade_id,
        customer_id=customer_id,
        user_id=cur_user_id,
        deadline=deadline,
    )
    db.add(new_black_list_db)
    db.commit()
    db.refresh(new_black_list_db)
    return new_black_list_db


def update_black_list(form, cur_user, db):
    if one_black_list(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli black_list mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    if debts.one_debt(form.trade_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    if one_customer(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
    db.query(Black_list).filter(Black_list.id == form.id).update({
        Black_list.money: form.money,
        Black_list.trade_id: form.trade_id,
        Black_list.customer_id: form.customer_id,
        Black_list.user_id: cur_user.id,
        Black_list.status: form.status
    })
    db.commit()
    return one_black_list(form.id, db)


def black_list_delete(id, db):
    if one_black_list(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli black_list mavjud emas")
    db.query(Black_list).filter(Black_list.id == id).update({
        Black_list.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
