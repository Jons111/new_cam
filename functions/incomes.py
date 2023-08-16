import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.customers import one_customer, sub_customer_debt
from functions.debts import one_debt

from functions.users import one_user

from models.incomes import Incomes

from utils.pagination import pagination


def all_incomes(search, status, trade_id, customer_id, user, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Incomes.money.like(search_formatted) | Incomes.type.like(search_formatted)
    else:
        search_filter = Incomes.id > 0
    if status in [True, False]:
        status_filter = Incomes.status == status
    else:
        status_filter = Incomes.status.in_([True, False])

    if trade_id:
        trade_id_filter = Incomes.trade_id == trade_id
    else:
        trade_id_filter = Incomes.trade_id > 0
    if customer_id:
        customer_id_filter = Incomes.customer_id == customer_id
    else:
        customer_id_filter = Incomes.customer_id > 0

    if user:
        user_filter = Incomes.user_id == user.id
    else:
        user_filter = Incomes.user_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    incomes = db.query(Incomes ).filter(Incomes.date > start_date).filter(
        Incomes.date <= end_date).filter(search_filter, customer_id_filter, status_filter, user_filter,
                                         trade_id_filter).order_by(
        Incomes.id.desc())
    if page and limit:
        return pagination(incomes, page, limit)

    else:
        return incomes.all()


def one_income(id, db):
    return db.query(Incomes).options(
        joinedload(Incomes.trade),joinedload(Incomes.customer)).filter(Incomes.id == id).first()


async def create_income(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")




    new_income_db =  Incomes(
        money=form.money,
        type=form.type,
        currency=form.currency,
        customer_id=form.customer_id,
        trade_id=form.trade_id,
        source=form.source,
        user_id=cur_user.id, )
    db.add(new_income_db)
    db.commit()
    db.refresh(new_income_db)
    sub_customer_debt(customer_id=form.customer_id, user_id=cur_user.id, db=db, income=form.money,
                      currency=form.currency)
    # try:
    #     phone = one_phone_via_source_id(source_id=trade.customer.id, db=db)
    #     tel = phone.number[1:]
    #     text = f""" Assalomu alaykum hurmatli mijoz sizning xarid qilgan {trade.model} nomli maxsulotingiz uchun {form.money}$  qabul qilindi, {trade.rest_money}$ qoldi """
    #     send_sms(tel=tel, text=text)
    # except Exception as x:
    #     raise HTTPException(status_code=400, detail=f"{x}")
    # # update lifetime status
    # update_lifetime_payment(trade_id=form.trade_id, money=form.money, user=cur_user, db=db)
    # # update trade and lifetime status
    #
    #
    # if trade.rest_money == 0:
    #     update_trade_and_lifetime_status(trade_id=form.trade_id, user=cur_user, db=db)
    #
    #
    #     try:
    #         phone = one_phone_via_source_id(source_id=trade.customer.id, db=db)
    #         tel = phone.number[1:]
    #         text = f""" Assalomu alaykum hurmatli mijoz {form.money}$  qabul qilindi,{trade.rest_money}$ qoldi.\nSavdo muvaffaqiyatli yakunlandi xaridingiz uchun rahmat!!! """
    #         send_sms(tel=tel, text=text)
    #     except Exception as x:
    #         raise HTTPException(status_code=400, detail=f"{x}")
    #

    return new_income_db


def update_income(form, cur_user, db):
    if one_income(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli income mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Incomes).filter(Incomes.id == form.id).update({
        Incomes.money: form.money,
        Incomes.type: form.type,
        Incomes.currency: form.currency,
        Incomes.source: form.source,
        Incomes.trade_id: form.trade_id,
        Incomes.customer_id: form.customer_id,
        Incomes.user_id: cur_user.id,
        Incomes.status: form.status
    })
    db.commit()
    return one_income(form.id, db)
