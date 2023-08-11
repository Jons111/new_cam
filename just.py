import requests
from fastapi import HTTPException

def get_token():
    url = "https://notify.eskiz.uz/api/auth/login"

    payload = {'email': 'xlutfullayev25@gmail.com',
               'password': 'WfA6T2AP9kjDQL0CXlyJQ2JqormudDwDI03PBS81'}
    files = [

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return response.json()


def send_sms(tel,text):


    url = "https://notify.eskiz.uz/api/message/sms/send"
    try:
        payload = {'mobile_phone': f'{tel}',
                   'message': f'{text}',
                   'from': '4546'}
        files = []
        with open('tokenfile.txt', 'r') as file:
            bearer_token = file.readline()
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        if response.status_code == 401:
            bearer_token = get_token()['data']['token']
            with open('tokenfile.txt', 'w') as file:
                file.write(bearer_token)
        print(response.text)
    except Exception as x:
        raise HTTPException(status_code=400,detail=f"{x}")
