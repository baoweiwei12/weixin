from datetime import datetime
from typing import List, Tuple
from sqlalchemy import Row, or_
from sqlalchemy.orm import Session
from app import schemas, models
from app.core import utils


def create_weixin_personel(
    db: Session, weixin_personnel: schemas.PersonnelCreate
) -> models.Personnel:
    db_weixin_personnel = models.Personnel(**weixin_personnel.model_dump())
    db.add(db_weixin_personnel)
    db.commit()
    db.refresh(db_weixin_personnel)
    return db_weixin_personnel


def get_weixin_personnel_by_wxid(db: Session, wxid: str) -> models.Personnel | None:
    return db.query(models.Personnel).filter(models.Personnel.wxid == wxid).first()


def update_weixin_personnel(
    db: Session, wxid: str, weixin_personnel: schemas.PersonnelUpdate
) -> models.Personnel | None:
    db_weixin_personnel = (
        db.query(models.Personnel).filter(models.Personnel.wxid == wxid).first()
    )
    update_data = weixin_personnel.model_dump(exclude_unset=True)
    if db_weixin_personnel is None:
        return None

    for key, value in update_data.items():
        setattr(db_weixin_personnel, key, value)
    db.commit()
    db.refresh(db_weixin_personnel)
    return db_weixin_personnel


def search_weixin_personnel(db: Session, search: str) -> List[models.Personnel] | None:
    db_weixin_personnel = (
        db.query(models.Personnel).filter(
            or_(
                models.Personnel.wechat_id.like(f"%{search}%"),
                models.Personnel.nickname.like(f"%{search}%"),
                models.Personnel.remark.like(f"%{search}%"),
            )
        )
    ).all()
    return db_weixin_personnel


def get_weixin_group_by_wxid(db: Session, wxid: str) -> models.Group | None:
    return db.query(models.Group).filter(models.Group.wxid == wxid).first()


def create_weixin_group(db: Session, weixin_group: schemas.GroupCreate) -> models.Group:
    db_weixin_group = models.Group(**weixin_group.model_dump())
    db.add(db_weixin_group)
    db.commit()
    db.refresh(db_weixin_group)
    return db_weixin_group


def update_weixin_group(
    db: Session, wxid: str, weixin_group: schemas.GroupUpdate
) -> models.Group | None:
    db_weixin_group = db.query(models.Group).filter(models.Group.wxid == wxid).first()
    if db_weixin_group is None:
        return None
    update_data = weixin_group.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_weixin_group, key, value)
    db.commit()
    db.refresh(db_weixin_group)
    return db_weixin_group


def is_task_group_personnel(db: Session, group_wxid: str, personnel_wxid: str) -> bool:
    db_task_personnel_config = (
        db.query(models.TaskPersonnelConfig)
        .filter(
            models.TaskPersonnelConfig.group_wxid == group_wxid,
            models.TaskPersonnelConfig.personnel_wxid == personnel_wxid,
        )
        .first()
    )
    if db_task_personnel_config is None:
        return False
    return True


def is_task_personnel(db: Session, personnel_wxid: str) -> bool:
    db_task_personnel_config = (
        db.query(models.TaskPersonnelConfig)
        .filter(models.TaskPersonnelConfig.personnel_wxid == personnel_wxid)
        .first()
    )
    if db_task_personnel_config is None:
        return False
    return True


def create_task_record(
    db: Session, task_record: schemas.TaskRecordCreate
) -> models.TaskRecord:
    db_task_record = models.TaskRecord(**task_record.model_dump())
    db.add(db_task_record)
    db.commit()
    db.refresh(db_task_record)
    return db_task_record


def get_unprocessed_task_records(
    db: Session,
):
    db_unprocessed_task_records = (
        db.query(models.TaskRecord)
        .filter(models.TaskRecord.is_processed == False)
        .all()
    )
    return db_unprocessed_task_records


def get_unprocessed_task_records_by_group_wxid(
    group_wxid: str,
    db: Session,
):
    db_unprocessed_task_records = (
        db.query(models.TaskRecord)
        .filter(
            models.TaskRecord.is_processed == False,
            models.TaskRecord.group_wxid == group_wxid,
            models.TaskRecord.message_type == schemas.WeChatMessageType.文字.value,
        )
        .all()
    )
    return db_unprocessed_task_records


def get_today_dutys(db: Session) -> List[models.Duty]:
    db_today_dutys = (
        db.query(models.Duty)
        .filter(
            models.Duty.start_time <= datetime.now(),
        )
        .all()
    )
    return db_today_dutys


def create_error_record(
    db: Session, error_record: schemas.ErrorRecordCreate
) -> models.ErrorRecord:
    db_error_record = models.ErrorRecord(**error_record.model_dump())
    db.add(db_error_record)
    db.commit()
    db.refresh(db_error_record)
    return db_error_record


# def get_error_records_by_
