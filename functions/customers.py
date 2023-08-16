from fastapi import HTTPException
from sqlalchemy.orm import joinedload


from models.phones import Phones
from models.debts import Debts
from models.users import Users
from models.incomes import Incomes
from models.customers import Customers

from utils.pagination import pagination


def all_customers(search, status, user, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Customers.name.like(search_formatted) | Phones.number.like(search_formatted)


    else:
        search_filter = Customers.id > 0

    if status in [True, False]:
        status_filter = Customers.status == status
    else:
        status_filter = Customers.status.in_([True, False])

    if user:
        user_id_filter = Customers.user_id == user.id
    else:
        user_id_filter = Customers.id > 0

    customers = db.query(Customers).join(Phones).options(
        joinedload(Customers.phone),joinedload(Customers.debt),joinedload(Customers.order),).filter(search_filter,
                                                        status_filter,
                                                        user_id_filter,
                                                        ).order_by(Customers.id.desc())

    if page and limit:
        return pagination(customers, page, limit)
    else:
        return customers.all()


def one_customer(id, db):
    return db.query(Customers).join(Phones).options(
        joinedload(Customers.phone),joinedload(Customers.debt),joinedload(Customers.order),).filter(Customers.id == id).first()


def create_customer(form, user, db):
    new_customer_db = Customers(
        name=form.name,
        last_name=form.last_name,
        user_id=user.id,
    )
    db.add(new_customer_db)
    db.commit()

    for phone in form.customer_phones:
        new_phone_db = Phones(
            number=phone.number,
            source_id=new_customer_db.id,
            source='customer',
            user_id=user.id
        )
        db.add(new_phone_db)
        db.commit()
    return new_customer_db


def update_customer(form, user, db):
    if one_customer(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mijoz mavjud emas")

    db.query(Customers).options(
        joinedload(Customers.phones).load_only(Phones.number)).filter(Customers.id == form.id).update({
        Customers.name: form.name,
        Customers.last_name: form.last_name,
        Customers.status: form.status,
        Customers.user_id: user.id,

    })
    db.commit()

    for phone in form.customer_phones:
        db.query(Phones).filter(Phones.id == phone.id).update({
            Phones.number: phone.number,
            Phones.source: 'customer',
            Phones.source_id: form.id,
            Phones.user_id: user.id
        })
        db.commit()

    return one_customer(form.id, db)


def customer_delete(id, user, db):
    if one_customer(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli customer mavjud emas")
    db.query(Customers).filter(Customers.id == id).update({
        Customers.status: False,
        Customers.user_id: user.id
    })
    db.commit()
    trades = db.query(Debts).filter(Debts.customer_id == id, Debts.debt_status == True).all()
    for trade in trades:
        db.query(Debts).filter(Debts.id == trade.id).update({
            Debts.status: False,
            Debts.user_id: user.id
        })
        db.commit()
        lifetimes = db.query(Incomes).filter(Incomes.customer_id == trade.id).all()
        for lifetime in lifetimes:
            db.query(Incomes).filter(Incomes.id == lifetime.id).update({
                Incomes.status: False,
                Incomes.user_id: user.id
            })
            db.commit()

    return {"date": "Customer o'chirildi !"}


def add_customer_debt(customer_id, user_id, db, debt, currency):
    customer = db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).first()
    if currency == 'uzs':
        debt = customer.debt + debt
        db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).update({
            Customers.debt: debt
        })
        db.commit()
    else:
        debt_usd = customer.debt_usd + debt
        db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).update({
            Customers.debt_usd: debt_usd
        })
        db.commit()


def sub_customer_debt(customer_id, user_id, db, income, currency):
    customer = db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).first()
    if currency == 'uzs':
        debt = customer.debt - income
        db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).update({
            Customers.debt: debt
        })
        db.commit()
    else:
        debt_usd = customer.debt_usd - income
        db.query(Customers).filter(Customers.id == customer_id, Users.id == user_id).update({
            Customers.debt_usd: debt_usd
        })
        db.commit()
