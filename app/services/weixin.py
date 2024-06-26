from fastapi import HTTPException
from pydantic import BaseModel
import requests
import logging

base_rul = "http://127.0.0.1:10010"


def send_text(receiver: str, msg: str, aters: str):
    try:
        url = base_rul + "/text"
        response = requests.post(
            url, json={"receiver": receiver, "msg": msg, "aters": aters}
        )
        response.raise_for_status()
        if response.json()["status"] == 0 and response.json()["data"] == True:
            logging.info(f"发送消息成功: {response.json()}")
            return True
        logging.info(f"发送消息失败: {response.json()}")
        return False
    except Exception as e:
        logging.error(f"发送消息出错: {e}  {response.text}")
        return False


def save_image(dir: str, extra: str, id: int):
    try:
        url = base_rul + "/save-image"
        json_data = {"dir": dir, "extra": extra, "id": id, "timeout": 10}
        response = requests.post(url, json=json_data)
        response.raise_for_status()
        if response.json()["status"] == 0 and (response.json()["data"] is not None):
            logging.info(f"保存图片成功: {dir}")
            image_path: str = response.json()["data"]
            return image_path
        logging.error(f"保存图片失败: {json_data} {response.json()}")
        return ""
    except Exception as e:
        logging.error(f"保存图片失败: {json_data} {response.json()} {e}")
        return ""


def get_bot_info():
    class BotInfo(BaseModel):
        wxid: str
        name: str
        mobile: str

    try:
        url = base_rul + "/userinfo"
        response = requests.get(url)
        data = response.json()["data"]
        return BotInfo(wxid=data["wxid"], name=data["name"], mobile=data["mobile"])
    except Exception as e:
        logging.error(f"获取机器人信息失败:{e}")
        raise HTTPException(status_code=500, detail="获取机器人信息失败")
