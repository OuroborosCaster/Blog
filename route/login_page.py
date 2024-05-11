from main import *
import traceback



@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/api/login", dependencies=[Depends(check_browser)])
async def login(request: Request, response: Response):
    try:
        uid = nickname = hashed_password = salt = 0
        data = await request.json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')


        if (username is None and email is None) or password is None:
            raise ValueError('JSON格式不匹配')

        if username is None:
            async with Session(engine) as session:
                statement = select(User.uid, User.nickname, User.hashed_password, User.salt).where(User.email == email)
                result = await session.exec(statement)
                user = result.first()


            if user is None:
                raise LookupError(f'请求的用户名 {username} 不存在')
            if user is not None:
                uid, nickname, hashed_password, salt = user

        if email is None:
            async with Session(engine) as session:
                statement = select(User.uid, User.nickname, User.hashed_password, User.salt).where(
                    func.binary(User.name) == username)
                result = await session.exec(statement)
                user = result.first()

            if user is None:
                raise LookupError(f'请求的电子邮箱 {email} 不存在')
            if user is not None:
                uid, nickname, hashed_password, salt = user
        is_authenticated = verify_password(password, salt, hashed_password)

        if not is_authenticated:
            raise RuntimeError(f'用户 {uid} 密码错误')

        iss = datetime.datetime.now(datetime.timezone.utc)
        exp = iss + datetime.timedelta(days=3)
        payload = {'iat': iss, 'nbf': iss, 'exp': exp, 'uid': uid, 'nickname': nickname}
        token = jwt.encode(payload, key=JWT_KEY, algorithm='HS256')

        response.set_cookie(key='user_jwt', value=token, httponly=False, expires=exp)

        return {"message": "User login successfully"}

    except LookupError as e:
        log_adt.info(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=404, detail='请求的用户不存在')
    except RuntimeError as e:
        log_adt.info(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=401, detail='密码错误')
    except (JSONDecodeError, ValueError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400, detail='提交了无效的数据')
    except sqlalchemy.exc.OperationalError as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=503, detail='数据库服务器不可用')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500, detail='意料外的错误，请联系管理员')


