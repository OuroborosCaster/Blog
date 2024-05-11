from main import *


@app.get("/article/create")
async def article_create(request: Request):
    return templates.TemplateResponse("article/create.html", {"request": request})


@app.post("/api/article/publish")
async def article_publish(request: Request):
    try:
        data = await request.json()

        bid = get_bid()
        user_id = get_payload(request)['uid']
        title = data.get('title')
        summary = data.get('summary', '')
        content = data.get('content')
        content_path = f'./user_data/blogs/{user_id}/{bid}.md'

        if title is not None and title != '' and content is not None and content != '':
            async with Session(engine) as session:
                new_blog = Blog(bid=bid, user_id=user_id, title=title, summary=summary, content_path=content_path)
                print(new_blog)
                session.add(new_blog)
                await session.commit()
            content_dir = os.path.dirname(content_path)
            if not os.path.exists(content_dir):
                os.makedirs(content_dir)
            async with aiofiles.open(content_path, 'w', encoding='utf-8') as f:
                await f.write(content)
            return {"message": "发布成功"}
        else:
            return JSONResponse(status_code=400, content={"detail": "提交的内容不符合规定，请检查或联系管理员"})

    except Exception as e:
        log_adt.error(f'{lineNum(e)} - {e}')
        log_err.exception(f'{lineNum(e)} - {e}')
