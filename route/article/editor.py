from main import *
from fastapi import File, UploadFile


@app.get("/editor")
async def md_editor(request: Request):
    try:
        user_jwt = request.cookies.get("user_jwt")
        if user_jwt is not None:
            payload = jwt.decode(user_jwt, JWT_KEY, algorithms=["HS256"])
            vditor_id = payload['uid']
            return templates.TemplateResponse("editor.html", {"request": request, "vditor_id": vditor_id})
        else:
            return JSONResponse(status_code=403, content={"detail": "请登录"})
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        log_adt.warning(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=403, detail='无效的凭证')
    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
        raise HTTPException(status_code=500, detail='意料外的错误，请联系管理员')


# @app.post('/api/editor/upload')
# async def file_upload(request: Request, file: UploadFile = File()):
#     try:
#         # body = await request.json()
#         # print(body)
#         # print(1)
#         file_contents = await file.read()
#         print(file.filename)
#         print(file.size)
#         return {"msg": "", "code": 0, "data": {"errFiles": '', 'url': '/user_data/blog_files/' + file.filename}}
#     except Exception as e:
#         log_adt.error(f'{lineNum(e)} - {e}')
#         log_err.exception(f'{lineNum(e)} - {e}')
#         raise HTTPException(status_code=500, detail='意料外的错误，请联系管理员')
