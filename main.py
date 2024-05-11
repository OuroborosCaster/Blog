from json import JSONDecodeError
from app_log import log_acc, log_err, log_adt,lineNum
from http import HTTPStatus
import sqlalchemy, os, aiofiles,datetime
import aiofiles.os
from fastapi import FastAPI, Request, HTTPException, Depends, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from sqlmodel import select, func
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession as Session
from orm import *
from settings import SESSION_KEY, JWT_KEY
from func import get_sid,get_payload,datetime_filter,get_bid,encrypt_password,verify_password
import jwt


class LoggingAccMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        acc_info = f"{access_time}: {request.state.real_ip} {request.scope['http_version']} {request.method} {request.url.path} - {request.headers.get('User-Agent')}"
        response = await call_next(request)
        log_acc.info(f"{response.status_code} {HTTPStatus(response.status_code).phrase} - {acc_info}")
        return response


class RealIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_real_ip = request.headers.get("X-Real-IP")
        if x_real_ip:
            # 如果存在X-Real-IP字段，取最左边的IP地址作为客户端真实IP
            request.state.real_ip = x_real_ip.split(",")[0]
        else:
            # 否则，从request.client.host获取IP地址
            request.state.real_ip = request.client.host
        response = await call_next(request)
        return response


app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.filters["datetime"] = datetime_filter
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY, max_age=600)
app.add_middleware(LoggingAccMiddleware)
app.add_middleware(RealIPMiddleware)


def check_browser(request: Request):
    if "browser" not in request.session or not request.session["browser"]:
        raise HTTPException(status_code=403, detail='会话过期，请刷新页面')


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.head("/")
async def root_head(request: Request):
    return Response()


@app.get("/session")
async def set_session(request: Request, response: Response):
    request.session.clear()  # 清除旧会话
    request.session["browser"] = True
    response.set_cookie(key='session_check', value=get_sid(), httponly=False, expires=540)
    return {"message": "Session is set"}


@app.get("/blogs")
async def blog_page(request: Request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(bid='1', title='Test Blog', summary=summary, created_at=time.time() - 120),
        Blog(bid='2', title='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(bid='3', title='Learn Swift', summary=summary, created_at=time.time() - 7200)
    ]
    return templates.TemplateResponse("blogs.html", {"request": request, 'blogs': blogs})


@app.get("/renew-login", dependencies=[Depends(check_browser)])
async def renewLoginCookie(request: Request, response: Response):
    user_jwt = request.cookies.get("user_jwt")
    try:
        # 解码 JWT
        payload = jwt.decode(user_jwt, JWT_KEY, algorithms=["HS256"])

        if payload['exp'] - payload['iat'] < 2592000:  # 检查距离上次登陆是否超过30日
            now = datetime.datetime.now(datetime.timezone.utc)
            payload['exp'] = min(int((now + datetime.timedelta(days=3)).timestamp()), payload['iat'] + 2592000)
            print(payload)
            token = jwt.encode(payload, key=JWT_KEY, algorithm='HS256')
            response.set_cookie(key='user_jwt', value=token, httponly=False, expires=payload['exp'])
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


import route
