from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime


class WeChatMessageType(Enum):
    朋友圈消息 = 0
    文字 = 1
    图片 = 3
    语音 = 34
    好友确认 = 37
    可能的好友消息 = 40
    名片 = 42
    视频 = 43
    石头剪刀布_表情图片 = 47
    位置 = 48
    共享实时位置_文件_转账_链接 = 49
    VOIP消息 = 50
    微信初始化 = 51
    VOIP通知 = 52
    VOIP邀请 = 53
    小视频 = 62
    微信红包 = 66
    系统通知 = 9999
    红包_系统消息 = 10000
    撤回消息 = 10002
    搜狗表情 = 1048625
    链接 = 16777265
    微信红包2 = 436207665
    红包封面 = 536936497
    视频号视频 = 754974769
    视频号名片 = 771751985
    引用消息 = 822083633
    拍一拍 = 922746929
    视频号直播 = 973078577
    商品链接 = 974127153
    视频号直播2 = 975175729
    音乐链接 = 1040187441
    文件 = 1090519089


class PersonnelBase(BaseModel):
    wxid: str
    wechat_id: str
    nickname: str
    remark: str


class PersonnelCreate(PersonnelBase):
    pass


class PersonnelUpdate(PersonnelBase):
    pass


class Personnel(PersonnelBase):
    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    wxid: str
    name: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    class Config:
        from_attributes = True


class TaskRecordBase(BaseModel):
    message_id: int
    group_wxid: str
    personnel_wxid: str
    content: str
    created_at: datetime
    message_type: int
    is_processed: bool
    attched_file: str | None = None
    processed_at: datetime | None = None


class TaskRecordCreate(TaskRecordBase):
    pass


class TaskRecordUpdate(TaskRecordBase):
    pass


class TaskRecord(TaskRecordBase):
    id: int

    class Config:
        from_attributes = True


class DutyBase(BaseModel):
    group_wxid: str
    personnel_wxid: str
    start_time: datetime
    end_time: datetime


class DutyCreate(DutyBase):
    pass


class DutyUpdate(DutyBase):
    pass


class Duty(DutyBase):
    id: int

    class Config:
        from_attributes = True


class ErrorRecordBase(BaseModel):
    group_wxid: str
    personnel_wxid: str
    recorder_wxid: str
    content: str
    recorded_at: datetime
    image_url: str


class ErrorRecordCreate(ErrorRecordBase):
    pass


class ErrorRecordUpdate(ErrorRecordBase):
    pass


class ErrorRecord(ErrorRecordBase):
    id: int

    class Config:
        from_attributes = True
