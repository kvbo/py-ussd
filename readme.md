# USSD-Router
Simple library to written with the motivation of working with ussd in a sane and concise way. This library is meant to be framework agnositic so that
you can use it with your favourite backend framework.
#### Under development
## Features
1. ### Routing                  (DONE)
    - Attach multiple routers defined in different files.
    - **MINOR TODO** improve attachment of routes
2. ### Validation               (ON GOING)
    - Ability to add validators to user input.
    - Allows the use of custom validators.
3. ### Middleware               (TODO)
4. ### Session Management       (TODO)

## Example usage
This example uses fast api but you can use any python framework of your own choosing or you need is an endpoint as an entry point to the ussd handler.
```
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import pydantic
import uvicorn
import urllib
from ussd import USSD

ussd = USSD()

# Define your routes
@ussd.route("")
def root(params):
    res = \
    """CON Welcome to mobopay. What can we do for you today.
        1. Check balance
        2. Send Money
    """
    return res

@ussd.route("1")
def check_balance(params):
    res = \
    """CON Enter Pin.
    """
    return res

@ussd.route("1*{pin}")
def check_balance_pin(params):
    if params["pin"] != '5322':
        res = f"""END Invalid pin
        """
    else:   
        res = \
        f"""END Your balance is ZMW 300.00
        """
    return res

@ussd.route("2")
def send_money(params):
    res = \
    """CON Enter number to send to.
    """
    return res

@ussd.route("2*{number:str}")
def send_money_enter_amount(params):
    return """CON Enter amount(ZMW)"""

@ussd.route("2*{number}*{amount:int}")
def send_money_enter_amount_p
in(params):
    return """CON Enter pin."""

@ussd.route("2*{number}*{amount}*{pin}")
def send_money_enter_amount_pin(params):
    print(params)
    if params["pin"] != '2345':
        return """END Invalid pin"""
    return f"""END Sending..."""


class UssdMessage(pydantic.BaseModel):
    sessionId : str | None =  None
    serviceCode  : str | None = None
    phoneNumber: str | None = None
    text         : str = ""

def parse(txt: str) -> UssdMessage:
    parsed_query = urllib.parse.parse_qs(txt)
    new_dict = {}
    for key, value in parsed_query.items():
        new_dict[key] = value[0]
    return UssdMessage(**new_dict)

app = FastAPI()

# Define end point to recieve ussd requests
@app.post("/ussd", response_class=PlainTextResponse)
async def u(req: Request):
    data = parse(str(await req.body(), encoding="utf-8").strip())
    res = ""
    try:
        # Handle ussd
        res = ussd.handler(data.text)      
    except Exception as e:
        raise HTTPException(500, str(e))
    return res
```
