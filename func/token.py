import jwt
from settings import JWT_KEY
from fastapi import  HTTPException
from app_log import  log_err, log_adt,lineNum
def get_payload(request):
    try:
        user_jwt = request.cookies.get("user_jwt")
        payload = jwt.decode(user_jwt, JWT_KEY, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=400, detail='身份验证出错，请重新登录')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500, detail='意料之外的错误，请联系管理员')