from func import encrypt_password
from main import *


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/api/check/username", dependencies=[Depends(check_browser)])
async def check_username(request: Request):
    try:
        data = await request.json()
        username = data.get("username")
        if username is None:
            raise ValueError('JSON格式不匹配')
        async with Session(engine) as session:
            statement = select(User.uid).where(func.binary(User.name) == username)
            result = await session.exec(statement)
            exist = result.first()
    except (JSONDecodeError, ValueError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400,detail='提交了无效的数据')
    except sqlalchemy.exc.OperationalError as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=503,detail='数据库服务器不可用')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500,detail='意料外的错误，请联系管理员')
    if exist:
        return {"isAvailable": False}
    else:
        return {"isAvailable": True}


@app.post("/api/check/nickname", dependencies=[Depends(check_browser)])
async def check_nickname(request: Request):
    try:
        data = await request.json()
        nickname = data.get("nickname")
        if nickname is None:
            raise ValueError('JSON格式不匹配')
        async with Session(engine) as session:
            statement = select(User.uid).where(func.binary(User.nickname) == nickname)
            result = await session.exec(statement)
            exist = result.first()
    except (JSONDecodeError, ValueError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400,detail='提交了无效的数据')
    except sqlalchemy.exc.OperationalError as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=503,detail='数据库服务器不可用')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500,detail='意料外的错误，请联系管理员')
    if exist:
        return {"isAvailable": False}
    else:
        return {"isAvailable": True}


@app.post("/api/check/email", dependencies=[Depends(check_browser)])
async def check_email(request: Request):
    try:
        data = await request.json()
        email = data.get("email")
        if email is None:
            raise ValueError('JSON格式不匹配')
        async with Session(engine) as session:
            statement = select(User.uid).where(User.email == email)
            result = await session.exec(statement)
            exist = result.first()
    except (JSONDecodeError, ValueError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400,detail='提交了无效的数据')
    except sqlalchemy.exc.OperationalError as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=503,detail='数据库服务器不可用')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500,detail='意料外的错误，请联系管理员')
    if exist:
        return {"isAvailable": False}
    else:
        return {"isAvailable": True}


@app.post("/api/register", dependencies=[Depends(check_browser)])
async def register(request: Request):
    try:
        data = await request.json()
        username = data.get('username')
        nickname = data.get('nickname')
        email = data.get('email')
        password = data.get('password')
        if username is None or email is None or password is None:
            raise ValueError('JSON格式不匹配')
        # 使用自定义函数生成盐和加密密码
        hashed_password, salt = encrypt_password(password)

        # 创建用户实例
        user = User(name=username, nickname=nickname, email=email, hashed_password=hashed_password, salt=salt)

        # 创建数据库会话
        async with Session(engine) as session:
            # 添加新用户到数据库
            session.add(user)
            await session.commit()

        return {"message": "User registered successfully"}
    except (JSONDecodeError, ValueError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400,detail='提交了无效的数据')
    except sqlalchemy.exc.OperationalError as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=503,detail='数据库服务器不可用')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500,detail='意料外的错误，请联系管理员')
