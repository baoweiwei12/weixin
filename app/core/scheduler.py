from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from app import crud, models, schemas
from app.core.database import SessionLocal
from app.services import weixin
import logging

scheduler = AsyncIOScheduler(timezone=pytz.utc)


def send_duty_message():
    logging.info("开始执行发送值日提醒任务")
    try:
        db = SessionLocal()

        today_dutys = crud.get_today_dutys(db)
        if len(today_dutys) == 0:
            return

        for duty in today_dutys:
            logging.info(
                f"发送值日提醒任务: {duty.group.name}--{duty.personnel.remark}--{duty.personnel.wxid}"
            )
            unprocessed_task_records = crud.get_unprocessed_task_records_by_group_wxid(
                str(duty.group_wxid), db
            )
            count = len(unprocessed_task_records)
            if count == 0:
                continue
            unprocessed_task_records_text = ""
            for task_record in unprocessed_task_records:
                unprocessed_task_records_text += f"{task_record.created_at} {task_record.personnel.remark}:{task_record.content}\n"
            text = f"""
@{duty.personnel.nickname},你好，{duty.personnel.remark},待处理的任务如下：

{unprocessed_task_records_text}

共{count}条任务。
"""
            weixin.send_text(str(duty.group_wxid), text, str(duty.personnel_wxid))
            logging.info(f"发送完成：{duty.group_wxid} {duty.personnel_wxid} {text}")
    except Exception as e:
        logging.error(e)
    finally:
        db.close()


scheduler.add_job(
    send_duty_message,
    trigger=CronTrigger(hour=18, minute=34, timezone="Asia/Shanghai"),
)
