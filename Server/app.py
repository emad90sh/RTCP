from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import redis

r = redis.Redis()
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/assets", StaticFiles(directory="templates"), name="templates")

def get_price_from_db():
    btc_price = r.get("btc_price")
    eth_price = r.get("eth_price")
    return {"btc": btc_price, "eth": eth_price}

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/price")
def get_price():
    return {
        'status': True,
        'data': get_price_from_db()
    }

