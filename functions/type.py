import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.debts import one_debt
from functions.users import one_user
from models.type import Types

from utils.pagination import pagination


def all_types(search, status,   start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Types.name.like(search_formatted)
    else:
        search_filter = Types.id > 0
    if status in [True, False]:
        status_filter = Types.status == status
    else:
        status_filter = Types.status.in_([True, False])


    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    types = db.query(Types).filter(Types.date > start_date).filter(
        Types.date <= end_date).filter(search_filter, status_filter,  ).order_by(
        Types.id.desc())
    if page and limit:
        return pagination(types, page, limit)

    else:
        return types.all()


def one_type(id, db):
    return db.query(Types).filter(Types.id == id).first()


async def create_type(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")



    new_type_db = Types(
        name=form.name,
        user_id=cur_user.id,

    )
    db.add(new_type_db)
    db.commit()
    db.refresh(new_type_db)

    return new_type_db


def update_type(form, cur_user, db):
    if one_type(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli type mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Types).filter(Types.id == form.id).update({
        Types.name: form.name,
        Types.user_id: cur_user.id,
        Types.status: form.status
    })
    db.commit()
    return one_type(form.id, db)
