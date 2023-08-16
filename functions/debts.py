import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.customers import one_customer
from functions.trades import one_trade
from functions.users import one_user



from models.debts import Debts

from utils.pagination import pagination



def all_debts(search, status, debt_status, customer_id, user, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Debts.money.like(search_formatted)

    else:
        search_filter = Debts.id > 0
    if status in [True, False]:
        status_filter = Debts.status == status
    else:
        status_filter = Debts.status.in_([True, False])
    if debt_status in [True, False]:
        debt_status_filter = Debts.debt_status == debt_status
    else:
        debt_status_filter = Debts.debt_status.in_([True, False])
    if customer_id:
        order_filter = Debts.customer_id == customer_id
    else:
        order_filter = Debts.customer_id > 0

    if user:
        user_filter = Debts.user_id == user.id
    else:
        user_filter = Debts.user_id > 0

    debts = db.query(Debts).options(
        joinedload(Debts.trade),joinedload(Debts.customer) ).filter(
        search_filter,
        status_filter,
        order_filter,
        user_filter,
        debt_status_filter
    ).order_by(Debts.id.desc())

    if page and limit:
        return pagination(debts, page, limit)
    else:
        return debts.all()


def one_debt(id, db):
    return db.query(Debts).options(
        joinedload(Debts.trade),joinedload(Debts.customer) ).filter(
        Debts.id == id).order_by(Debts.id.desc()).first()


def last_debt(user_id, db):
    return db.query(Debts).filter(Debts.user_id == user_id).order_by(Debts.id.desc()).first()


def one_debt_via_debt_id(debt_id, db):
    return db.query(Debts).filter(
        Debts.debt_id == debt_id).first()


def create_debt(form, user, db):
    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
    if one_customer(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
    if one_trade(form.trade_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
    # if functions.black_list.check_black_list(form.customer_id, db):
    #     raise HTTPException(status_code=400, detail="Qora ro'yxatga tushgan mijoz bilan savdo amalga oshirmaydi")
    # if not form.deadline:
    #     raise HTTPException(status_code=400, detail="To'lov muddatini (oy) kiriting ")
    # try:
    #     debt = last_debt(user.id, db=db)
    #
    #     if debt:
    #         year = datetime.datetime.now().year
    #         number = str(debt.debt_number).split('/')
    #         debt_number = f"{year}/{int(number[1]) + 1}"
    #     else:
    #         year = datetime.datetime.now().year
    #         debt_number = f"{year}/{1}"
    new_debt_db = Debts(

            customer_id=form.customer_id,
            trade_id=form.trade_id,
            money=form.money,
            currency=form.currency,
            user_id=user.id,
            deadline=form.deadline,


        )

    db.add(new_debt_db)
    db.commit()
    db.refresh(new_debt_db)
    # except Exception as x:
    #     raise HTTPException(status_code=400, detail=f"{x}")
    # add_customer_debt(customer_id=form.customer_id,user_id=user.id,db=db,debt=form.money,currency=form.currency)
    return new_debt_db

    # try:
    #     phone = one_phone_via_source_id(source_id=form.customer_id, db=db)
    #     tel = phone.number[1:]
    #     end_date = datetime.datetime.strftime((form.date), '%d-%m-%Y')
    #     text = f""" Assalomu alaykum, {form.name}. Sizga {end_date} - yili\nNomi : {form.model}\nRangi : {form.color} rangli\nImei : {form.imei} telefoni\nNarxi : {form.given_price}$ ga\nDastlabki to'lov : {form.first_payment}$\nMuddati : {form.sms} oy muddatga\nOylik to'lov : {format(form.rest_money / form.sms, '.2f')}$ dan nasiya savdo qilib baraka qildik """
    #     send_debt(tel=tel, text=text)
    # except Exception as x:
    #     raise HTTPException(status_code=400, detail=f"{x} ")

    # add sms section


def update_debt(form, user, db):
    if one_debt(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Debts).filter(Debts.id == form.id).update({
        Debts.id: form.id,
        Debts.customer_id: form.customer_id,
        Debts.trade_id: form.trade_id,
        Debts.status: form.status,
        Debts.money: form.money,
        Debts.currency: form.currency,
        Debts.deadline: form.deadline,
        Debts.date: form.date,
        Debts.debt_status: form.debt_status,
        Debts.user_id: user.id})
    db.commit()

    # rest_money = form.quantity * form.given_price - form.first_payment
    # try:
    #     money = rest_money / form.sms
    #
    #     smss = db.query(Sms).filter(Sms.debt_id == form.id).all()
    #     for life in smss:
    #         db.query(Sms).filter(Sms.id == life.id).update({
    #             Sms.price: money})
    #         db.commit()
    #
    #
    # except Exception as x:
    #     raise HTTPException(status_code=400, detail=f"{x}   To'lov muddatini (oy) kiriting ")
    return one_debt(form.id, db)


def filter_debts(order_id, db, status=True):
    if status in [True, False]:
        status_filter = Debts.debt_status == status
    else:
        status_filter = Debts.id > 0

    if order_id:
        order_filter = Debts.order_id == order_id
    else:
        order_filter = Debts.id > 0

    users = db.query(Debts).filter(status_filter, order_filter).order_by(Debts.id.desc())

    return users.all()


def get_deadline_from_debts(order_id, user_id, db):
    if one_debt(order_id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")


# def update_debt_received_money(debt_id, money, user, db):
#     if one_debt(debt_id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
#
#     if one_user(user.id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
#     debt = one_debt(id=debt_id, db=db)
#     rest_money = debt.rest_money - money
#     received_money = debt.received_money + money
#     db.query(Debts).filter(Debts.id == debt_id).update({
#
#         Debts.rest_money: rest_money,
#         Debts.received_money: received_money,
#         Debts.user_id: user.id})
#     db.commit()
#     if debt.real_price < received_money:
#         profit = received_money - debt.real_price
#         db.query(Debts).filter(Debts.id == debt_id).update({
#
#             Debts.profit: profit,
#             Debts.user_id: user.id})
#     return one_debt(debt_id, db)


# def update_debt_received_money_back(debt_id, money, user, db):
#     if one_debt(debt_id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
#
#     if one_user(user.id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
#     debt = one_debt(id=debt_id, db=db)
#     rest_money = debt.rest_money - money
#     received_money = debt.received_money + money
#     db.query(Debts).filter(Debts.id == debt_id).update({
#
#         Debts.rest_money: rest_money,
#         Debts.received_money: received_money,
#         Debts.user_id: user.id})
#     db.commit()
#
#
# def update_debt_and_sms_status(debt_id, user, db):
#     if one_debt(debt_id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
#
#     if one_user(user.id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
#
#     db.query(Debts).filter(Debts.id == debt_id).update({
#         Debts.debt_status: False, })
#     db.commit()
#     smss = db.query(Sms).filter(Sms.debt_id == debt_id).order_by(
#         Sms.id.asc()).all()
#
#     for sms in smss:
#         db.query(Sms).filter(Sms.id == sms.id).update({
#             Sms.status: False, })
#         db.commit()


def debt_result(user, start_date, end_date, db):
    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.max

    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    if user:
        user_status = Debts.user_id == user.id
    else:
        user_status = Debts.id > 0

    debts = db.query(Debts).filter(Debts.date >= start_date).filter(Debts.date <= end_date).filter(
        user_status, Debts.status == True).all()

    real_price = 0
    given_price = 0
    rest_money = 0
    profit = 0
    received_money = 0
    for debt in debts:
        real_price += debt.real_price
        given_price += debt.given_price
        rest_money += debt.rest_money
        profit += debt.profit
        received_money += debt.received_money
    data = {
        "real_price": real_price,
        "given_price": given_price,
        "rest_money": rest_money,
        "profit": profit,
        "received_money": received_money,
    }
    return data
