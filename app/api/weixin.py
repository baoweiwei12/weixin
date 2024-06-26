from datetime import datetime
from enum import Enum
import logging
import shutil
from typing import Optional
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
    Query,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import dependencies, security
from app.services import weixin
import os

router = APIRouter(prefix="", tags=["weixin"])


class WxMessage(BaseModel):
    is_self: bool
    is_group: bool
    id: int
    type: int
    ts: int
    roomid: str
    content: str
    sender: str
    sign: str
    thumb: str
    extra: str
    xml: str


@router.post("/weixin/webhook")
def weixin_webhook(message: WxMessage, db: Session = Depends(dependencies.get_db)):
    logging.info(f"收到消息：{message}")
    logging.info(f"消息类型：{schemas.WeChatMessageType(message.type).name}")
    if message.is_group and crud.is_task_group_personnel(
        db=db, group_wxid=message.roomid, personnel_wxid=message.sender
    ):
        logging.info(f"处理任务消息")
        attched_file = None
        if message.type == schemas.WeChatMessageType.图片.value:
            attched_file_dir = os.getcwd().replace("\\", "/") + "/attched-file/images"
            attched_file_path = weixin.save_image(
                dir=attched_file_dir,
                extra=message.extra,
                id=message.id,
            )
            file_name = attched_file_path.split("/")[-1]
            attched_file = f"/weixin/attched-file/images/{file_name}"

        crud.create_task_record(
            db=db,
            task_record=schemas.TaskRecordCreate(
                group_wxid=message.roomid,
                personnel_wxid=message.sender,
                content=message.content,
                message_type=message.type,
                message_id=message.id,
                created_at=datetime.now(),
                is_processed=False,
                attched_file=attched_file,
            ),
        )
    if message.is_group and message.content == f"@{weixin.get_bot_info().name}\u2005":
        text = f"""
{weixin.get_bot_info().name}为您服务。
点击链接提交错误记录:http://192.168.251.70:8000/weixin/errors?group_wxid={message.roomid}&recorder_wxid={message.sender}
"""
        weixin.send_text(
            message.roomid,
            text,
            message.sender,
        )

    return {"status": 0, "message": "成功"}


@router.get("/weixin/personnel")
def get_weixin_personnel(
    db: Session = Depends(dependencies.get_db), search: str = Query("")
):
    return crud.search_weixin_personnel(db, search)


@router.get("/weixin/errors")
def get_weixin_errors(
    group_wxid: str = Query(),
    recorder_wxid: str = Query(),
    db: Session = Depends(dependencies.get_db),
):
    group = crud.get_weixin_group_by_wxid(db, group_wxid)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    recorder = crud.get_weixin_personnel_by_wxid(db, recorder_wxid)
    if recorder is None:
        raise HTTPException(status_code=404, detail="Recorder not found")
    with open("./app/templates/errorform.html", "r", encoding="utf-8") as f:
        html = f.read()
        return HTMLResponse(html)


@router.post("/weixin/error/submit")
async def submit_form(
    errorContent: str = Form(...),
    personnel_wxid: str = Form(...),
    group_wxid: str = Form(...),
    recorder_wxid: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(dependencies.get_db),
):
    if (
        crud.get_weixin_personnel_by_wxid(db, personnel_wxid)
        and crud.get_weixin_group_by_wxid(db, group_wxid)
        and crud.get_weixin_personnel_by_wxid(db, recorder_wxid)
    ) == False:
        raise HTTPException(status_code=400, detail="人员或群组不存在")

    max_file_size = 2 * 1024 * 1024
    if file:
        file_size = await file.read()
        if len(file_size) > max_file_size:
            raise HTTPException(status_code=400, detail="图片大小不能超过 2MB")
        file.file.seek(0)
        valid_image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
        file_extension = file.filename.split(".")[-1].lower()  # type: ignore

        if f".{file_extension}" not in valid_image_extensions:
            raise HTTPException(status_code=400, detail="只能上传图片文件")

    UPLOAD_DIR = "./attched-file/images"
    try:
        # 保存文件
        if file:
            file_path = f"{UPLOAD_DIR}/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        if file:
            image_url = f"/weixin/attched-file/images/{file.filename}"

        crud.create_error_record(
            db,
            schemas.ErrorRecordCreate(
                group_wxid=group_wxid,
                personnel_wxid=personnel_wxid,
                recorder_wxid=recorder_wxid,
                content=errorContent,
                recorded_at=datetime.now(),
                image_url=image_url,
            ),
        )

        return {"status": 0, "message": "成功"}

    except Exception as e:
        print(f"提交表单出错: {e}")
        raise HTTPException(status_code=500, detail="提交表单失败")
