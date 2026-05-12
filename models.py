from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid

class FrequencyEnum(str, Enum):
    """提醒频率类型"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class NotificationTypeEnum(str, Enum):
    """通知类型"""
    SYSTEM = "system"
    EMAIL = "email"
    WEBHOOK = "webhook"

class Reminder:
    """提醒任务模型"""
    
    def __init__(
        self,
        title: str,
        description: str = "",
        remind_date: Optional[str] = None,
        remind_time: str = "09:00",
        frequency: str = "once",
        notification_types: List[str] = None,
        is_active: bool = True,
        reminder_id: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        last_triggered: Optional[str] = None
    ):
        self.id = reminder_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.remind_date = remind_date
        self.remind_time = remind_time
        self.frequency = frequency
        self.notification_types = notification_types or ["system"]
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.last_triggered = last_triggered
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "remind_date": self.remind_date,
            "remind_time": self.remind_time,
            "frequency": self.frequency,
            "notification_types": self.notification_types,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_triggered": self.last_triggered
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建Reminder对象"""
        return Reminder(
            title=data.get("title"),
            description=data.get("description", ""),
            remind_date=data.get("remind_date"),
            remind_time=data.get("remind_time", "09:00"),
            frequency=data.get("frequency", "once"),
            notification_types=data.get("notification_types", ["system"]),
            is_active=data.get("is_active", True),
            reminder_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            last_triggered=data.get("last_triggered")
        )
