import json
import os
from typing import List, Optional
from datetime import datetime
from config import config
from models import Reminder
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def ensure_data_dir():
    """确保数据目录存在"""
    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)

def load_reminders() -> List[Reminder]:
    """从文件加载所有提醒"""
    ensure_data_dir()
    
    if not os.path.exists(config.REMINDERS_FILE):
        return []
    
    try:
        with open(config.REMINDERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Reminder.from_dict(item) for item in data]
    except Exception as e:
        print(f"Error loading reminders: {e}")
        return []

def save_reminders(reminders: List[Reminder]):
    """将提醒保存到文件"""
    ensure_data_dir()
    
    try:
        with open(config.REMINDERS_FILE, 'w', encoding='utf-8') as f:
            data = [reminder.to_dict() for reminder in reminders]
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving reminders: {e}")

def get_reminder_by_id(reminder_id: str) -> Optional[Reminder]:
    """根据ID获取提醒"""
    reminders = load_reminders()
    for reminder in reminders:
        if reminder.id == reminder_id:
            return reminder
    return None

def send_email_notification(reminder: Reminder):
    """发送邮件通知"""
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        print("Email not configured")
        return False
    
    try:
        message = MIMEMultipart()
        message['From'] = config.SMTP_USER
        message['To'] = config.SMTP_USER
        message['Subject'] = f"提醒: {reminder.title}"
        
        body = f"""
时间到了！

提醒: {reminder.title}
描述: {reminder.description}

请及时处理。
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"Email sent for reminder: {reminder.title}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_webhook_notification(reminder: Reminder):
    """发送Webhook通知"""
    if not config.WEBHOOK_URL:
        print("Webhook not configured")
        return False
    
    try:
        payload = {
            "id": reminder.id,
            "title": reminder.title,
            "description": reminder.description,
            "triggered_at": datetime.now().isoformat()
        }
        
        response = requests.post(config.WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"Webhook sent for reminder: {reminder.title}")
            return True
        else:
            print(f"Webhook failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending webhook: {e}")
        return False

def send_system_notification(reminder: Reminder):
    """发送系统通知（控制台输出）"""
    message = f"""
╔════════════════════════════════════╗
║ 🔔 提醒通知                        ║
╠════════════════════════════════════╣
║ 标题: {reminder.title:<20} ║
║ 描述: {reminder.description:<20} ║
║ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ║
╚════════════════════════════════════╝
    """
    print(message)
    return True

def trigger_reminder(reminder: Reminder):
    """触发提醒通知"""
    for notification_type in reminder.notification_types:
        if notification_type == "email":
            send_email_notification(reminder)
        elif notification_type == "webhook":
            send_webhook_notification(reminder)
        else:  # system
            send_system_notification(reminder)
    
    # 更新最后触发时间
    reminder.last_triggered = datetime.now().isoformat()
    reminder.updated_at = datetime.now().isoformat()
    
    reminders = load_reminders()
    for i, r in enumerate(reminders):
        if r.id == reminder.id:
            reminders[i] = reminder
            break
    save_reminders(reminders)
