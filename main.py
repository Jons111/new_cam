from fastapi import FastAPI


from routes import auth, users, phones, customers,  incomes, uploaded_files, debt, black_list,type,orders,trades,products,storage,zapchast

from db import Base, engine


Base.metadata.create_all(bind=engine)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = FastAPI(
    title="Savdo market",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],

)

app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],

)

app.include_router(
    phones.router_phone,
    prefix='/phone',
    tags=['Phone section'],

)

app.include_router(
    customers.router_customer,
    prefix='/customer',
    tags=['Customer section'],

)
app.include_router(
    orders.router_order,
    prefix='/order',
    tags=['Orders section'],

)
app.include_router(
    trades.router_trade,
    prefix='/trade',
    tags=['Trade section'],

)
app.include_router(
    storage.router_storage,
    prefix='/storage',
    tags=['Storage section'],

)
app.include_router(
    zapchast.router_zapchast,
    prefix='/zapchast',
    tags=['Zapchast section'],

)
app.include_router(
    products.router_product,
    prefix='/product',
    tags=['Product section'],

)




app.include_router(
    debt.router_debt,
    prefix='/debt',
    tags=['Debt section'],

)

app.include_router(
    incomes.router_income,
    prefix='/income',
    tags=['Income section'],

)

app.include_router(
    uploaded_files.router_file,
    prefix='/file',
    tags=['File  section'],

)

app.include_router(
    type.router_type,
    prefix='/type',
    tags=['Type  section'],

)

 
# try:
#     scheduler = BackgroundScheduler()
#
#
#     scheduler.add_job(check_lifetimes_yesterday, 'interval', seconds=120 )
#
#     scheduler.add_job(check_lifetimes_today, 'interval', seconds=120 )
#     scheduler.add_job(check_lifetimes, 'interval', seconds=120)
#     scheduler.add_job(check_lifetimes_tomorrow, 'interval', seconds=120)
#     scheduler.add_job(check_lifetimes_10days, 'interval', seconds=120)
#
#     scheduler.start()
# except Exception as x:
#     print(x)
#     with open("text.txt",'a') as file:
#         file.write(f"{x}   xatolik  \n")