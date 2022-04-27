import uvicorn
from fastapi import FastAPI, Depends, Body
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_bearer import JWTBearer
from app.database import db_handler_query
from app.models import UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
import json
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


def check_user(data: UserLoginSchema):
    f = open('app/users.json')
    user = json.load(f)
    if user['email'] == data.email and user['password'] == data.password:
        return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Wrong login details!"}


@app.get("/hello/{name}")
async def say_hello(name: str, token: str = Depends(oauth2_scheme)):
    bar = token
    prices = db_handler_query()

    return {"message": f"Hello {name}"}


@app.get("/price/{currency}", dependencies=[Depends(JWTBearer())])
async def get_last_price(currency: str):
    if currency == 'MX' or currency == 'mx':
        rates = {}
        results = db_handler_query()
        for price in results:
            rate = {
                f'provider_{price[4]}':{
                    "last_updated": price[1],
                    "time_registered": price[2],
                    "value": price[3]
                }
            }
            rates.update(rate)
        return {"rates": rates}
    else:
        return {"Not Work": "Not Work"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
    bar = 1
