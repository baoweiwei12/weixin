from typing import List
import requests
from app.core.database import SessionLocal
from app.crud import (
    get_weixin_personnel_by_wxid,
    create_weixin_personel,
    update_weixin_personnel,
    get_weixin_group_by_wxid,
    create_weixin_group,
    update_weixin_group,
)
from app.schemas import PersonnelCreate, PersonnelUpdate, GroupCreate, GroupUpdate

response = requests.get("http://127.0.0.1:10010/contacts")
data: List = response.json()["data"]["contacts"]
try:
    db = SessionLocal()
    for item in data:
        if "@" not in item["wxid"]:
            person = get_weixin_personnel_by_wxid(db, item["wxid"])
            if person is None:
                create_weixin_personel(
                    db,
                    PersonnelCreate(
                        wxid=item["wxid"],
                        wechat_id=item["code"],
                        nickname=item["name"],
                        remark=item["remark"],
                    ),
                )
                print(
                    f"添加人员成功 {item['name']} {item['wxid']} {item['code']} {item['remark']}"
                )
            else:
                update_weixin_personnel(
                    db=db,
                    wxid=item["wxid"],
                    weixin_personnel=PersonnelUpdate(
                        wxid=item["wxid"],
                        wechat_id=item["code"],
                        nickname=item["name"],
                        remark=item["remark"],
                    ),
                )
                print(
                    f"更新人员成功 {item['name']} {item['wxid']} {item['code']} {item['remark']}"
                )
        if item["wxid"].endswith("@chatroom"):
            group = get_weixin_group_by_wxid(db, item["wxid"])
            if group is None:
                create_weixin_group(
                    db,
                    GroupCreate(
                        wxid=item["wxid"],
                        name=item["name"],
                    ),
                )
                print(
                    f"创建群组成功 {item['name']} {item['wxid']} {item['code']} {item['remark']}"
                )
            else:
                update_weixin_group(
                    db,
                    item["wxid"],
                    GroupUpdate(
                        wxid=item["wxid"],
                        name=item["name"],
                    ),
                )
                print(
                    f"更新群组成功 {item['name']} {item['wxid']} {item['code']} {item['remark']}"
                )


finally:
    db.close()
