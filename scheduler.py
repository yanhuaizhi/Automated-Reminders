from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from models import Reminder
from utils import load_reminders, trigger_reminder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReminderScheduler:
    """提醒调度器"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.jobs = {}
    
    def start(self):
        """启动调度器"""
        if not self.scheduler.running:
            self.scheduler.start()
            self.load_reminders()
            logger.info("Scheduler started")
    
    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def load_reminders(self):
        """加载所有活动的提醒到调度器"""
        reminders = load_reminders()
        for reminder in reminders:
            if reminder.is_active:
                self.add_reminder(reminder)
    
    def add_reminder(self, reminder: Reminder):
        """添加提醒到调度器"""
        try:
            # 移除旧的任务
            if reminder.id in self.jobs:
                self.scheduler.remove_job(reminder.id)
            
            # 解析时间
            time_parts = reminder.remind_time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            
            # 根据频率添加任务
            if reminder.frequency == "once":
                # 一次性提醒
                if reminder.remind_date:
                    date_parts = reminder.remind_date.split('-')
                    year = int(date_parts[0])
                    month = int(date_parts[1])
                    day = int(date_parts[2])
                    
                    trigger = CronTrigger(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=minute
                    )
                else:
                    # 如果没有日期，使用今天
                    trigger = CronTrigger(hour=hour, minute=minute)
            
            elif reminder.frequency == "daily":
                trigger = CronTrigger(hour=hour, minute=minute)
            
            elif reminder.frequency == "weekly":
                trigger = CronTrigger(day_of_week='*', hour=hour, minute=minute)
            
            elif reminder.frequency == "monthly":
                trigger = CronTrigger(day=1, hour=hour, minute=minute)
            
            else:
                logger.warning(f"Unknown frequency: {reminder.frequency}")
                return
            
            job = self.scheduler.add_job(
                self.trigger_callback,
                trigger=trigger,
                id=reminder.id,
                args=[reminder],
                replace_existing=True
            )
            
            self.jobs[reminder.id] = job
            logger.info(f"Added reminder to scheduler: {reminder.title}")
        
        except Exception as e:
            logger.error(f"Error adding reminder to scheduler: {e}")
    
    def remove_reminder(self, reminder_id: str):
        """从调度器中移除提醒"""
        try:
            if reminder_id in self.jobs:
                self.scheduler.remove_job(reminder_id)
                del self.jobs[reminder_id]
                logger.info(f"Removed reminder from scheduler: {reminder_id}")
        except Exception as e:
            logger.error(f"Error removing reminder from scheduler: {e}")
    
    def trigger_callback(self, reminder: Reminder):
        """调度器触发的回调函数"""
        logger.info(f"Triggering reminder: {reminder.title}")
        trigger_reminder(reminder)
    
    def update_reminder(self, reminder: Reminder):
        """更新调度器中的提醒"""
        self.add_reminder(reminder)

# 全局调度器实例
reminder_scheduler = ReminderScheduler()
