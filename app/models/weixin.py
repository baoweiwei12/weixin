from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    BigInteger,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Personnel(Base):
    __tablename__ = "personnel"

    wxid = Column(String(255), primary_key=True)
    wechat_id = Column(String(255))
    nickname = Column(String(255))
    remark = Column(String(255))


class Group(Base):
    __tablename__ = "group"

    wxid = Column(String(255), primary_key=True)
    name = Column(String(255))


class TaskPersonnelConfig(Base):
    __tablename__ = "task_personnel_config"

    group_wxid = Column(String(255), ForeignKey("group.wxid"), primary_key=True)
    personnel_wxid = Column(String(255), ForeignKey("personnel.wxid"), primary_key=True)


class TaskRecord(Base):
    __tablename__ = "task_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger)
    group_wxid = Column(String(255), ForeignKey("group.wxid"))
    personnel_wxid = Column(String(255), ForeignKey("personnel.wxid"))
    content = Column(Text)
    message_type = Column(Integer)
    created_at = Column(DateTime)
    is_processed = Column(Boolean)
    attched_file = Column(String(255), nullable=True)
    processed_at = Column(DateTime, nullable=True)

    group = relationship("Group", primaryjoin="TaskRecord.group_wxid == Group.wxid")
    personnel = relationship(
        "Personnel", primaryjoin="TaskRecord.personnel_wxid == Personnel.wxid"
    )


class ErrorRecord(Base):
    __tablename__ = "error_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_wxid = Column(String(255), ForeignKey("group.wxid"))
    personnel_wxid = Column(String(255), ForeignKey("personnel.wxid"))
    recorder_wxid = Column(String(255), ForeignKey("personnel.wxid"))
    content = Column(Text)
    recorded_at = Column(DateTime)
    image_url = Column(String(255))

    group = relationship("Group", primaryjoin="ErrorRecord.group_wxid == Group.wxid")
    personnel = relationship(
        "Personnel", primaryjoin="ErrorRecord.personnel_wxid == Personnel.wxid"
    )


class Duty(Base):
    __tablename__ = "duty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_wxid = Column(String(255), ForeignKey("group.wxid"))
    personnel_wxid = Column(String(255), ForeignKey("personnel.wxid"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    personnel = relationship(
        "Personnel", primaryjoin="Duty.personnel_wxid == Personnel.wxid"
    )
    group = relationship("Group", primaryjoin="Duty.group_wxid == Group.wxid")
