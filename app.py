from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import Reminder
from utils import (
    load_reminders,
    save_reminders,
    get_reminder_by_id,
    trigger_reminder
)
from scheduler import reminder_scheduler
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 启动调度器
reminder_scheduler.start()

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    """获取所有提醒"""
    try:
        reminders = load_reminders()
        return jsonify({
            "success": True,
            "data": [r.to_dict() for r in reminders],
            "count": len(reminders)
        })
    except Exception as e:
        logger.error(f"Error getting reminders: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders/<reminder_id>', methods=['GET'])
def get_reminder(reminder_id):
    """获取单个提醒"""
    try:
        reminder = get_reminder_by_id(reminder_id)
        if reminder:
            return jsonify({"success": True, "data": reminder.to_dict()})
        else:
            return jsonify({"success": False, "error": "Reminder not found"}), 404
    except Exception as e:
        logger.error(f"Error getting reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders', methods=['POST'])
def create_reminder():
    """创建新提醒"""
    try:
        data = request.get_json()
        
        # 验证必要字段
        if not data.get('title'):
            return jsonify({"success": False, "error": "Title is required"}), 400
        
        reminder = Reminder(
            title=data.get('title'),
            description=data.get('description', ''),
            remind_date=data.get('remind_date'),
            remind_time=data.get('remind_time', '09:00'),
            frequency=data.get('frequency', 'once'),
            notification_types=data.get('notification_types', ['system']),
            is_active=data.get('is_active', True)
        )
        
        reminders = load_reminders()
        reminders.append(reminder)
        save_reminders(reminders)
        
        # 添加到调度器
        reminder_scheduler.add_reminder(reminder)
        
        logger.info(f"Created reminder: {reminder.title}")
        return jsonify({"success": True, "data": reminder.to_dict()}), 201
    
    except Exception as e:
        logger.error(f"Error creating reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders/<reminder_id>', methods=['PUT'])
def update_reminder(reminder_id):
    """更新提醒"""
    try:
        data = request.get_json()
        reminders = load_reminders()
        
        reminder = None
        for i, r in enumerate(reminders):
            if r.id == reminder_id:
                reminder = r
                break
        
        if not reminder:
            return jsonify({"success": False, "error": "Reminder not found"}), 404
        
        # 更新字段
        reminder.title = data.get('title', reminder.title)
        reminder.description = data.get('description', reminder.description)
        reminder.remind_date = data.get('remind_date', reminder.remind_date)
        reminder.remind_time = data.get('remind_time', reminder.remind_time)
        reminder.frequency = data.get('frequency', reminder.frequency)
        reminder.notification_types = data.get('notification_types', reminder.notification_types)
        reminder.is_active = data.get('is_active', reminder.is_active)
        reminder.updated_at = datetime.now().isoformat()
        
        save_reminders(reminders)
        
        # 更新调度器
        reminder_scheduler.update_reminder(reminder)
        
        logger.info(f"Updated reminder: {reminder.title}")
        return jsonify({"success": True, "data": reminder.to_dict()})
    
    except Exception as e:
        logger.error(f"Error updating reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders/<reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """删除提醒"""
    try:
        reminders = load_reminders()
        new_reminders = [r for r in reminders if r.id != reminder_id]
        
        if len(new_reminders) == len(reminders):
            return jsonify({"success": False, "error": "Reminder not found"}), 404
        
        save_reminders(new_reminders)
        
        # 从调度器中移除
        reminder_scheduler.remove_reminder(reminder_id)
        
        logger.info(f"Deleted reminder: {reminder_id}")
        return jsonify({"success": True, "message": "Reminder deleted"})
    
    except Exception as e:
        logger.error(f"Error deleting reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders/<reminder_id>/trigger', methods=['POST'])
def manual_trigger(reminder_id):
    """手动触发提醒"""
    try:
        reminder = get_reminder_by_id(reminder_id)
        if not reminder:
            return jsonify({"success": False, "error": "Reminder not found"}), 404
        
        trigger_reminder(reminder)
        logger.info(f"Manually triggered reminder: {reminder.title}")
        return jsonify({"success": True, "message": "Reminder triggered"})
    
    except Exception as e:
        logger.error(f"Error triggering reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders/<reminder_id>/toggle', methods=['POST'])
def toggle_reminder(reminder_id):
    """切换提醒状态"""
    try:
        reminders = load_reminders()
        
        reminder = None
        for r in reminders:
            if r.id == reminder_id:
                reminder = r
                break
        
        if not reminder:
            return jsonify({"success": False, "error": "Reminder not found"}), 404
        
        reminder.is_active = not reminder.is_active
        reminder.updated_at = datetime.now().isoformat()
        
        save_reminders(reminders)
        
        # 更新调度器
        if reminder.is_active:
            reminder_scheduler.add_reminder(reminder)
        else:
            reminder_scheduler.remove_reminder(reminder_id)
        
        logger.info(f"Toggled reminder: {reminder.title}")
        return jsonify({"success": True, "data": reminder.to_dict()})
    
    except Exception as e:
        logger.error(f"Error toggling reminder: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计信息"""
    try:
        reminders = load_reminders()
        active_count = sum(1 for r in reminders if r.is_active)
        inactive_count = len(reminders) - active_count
        
        freq_count = {}
        for r in reminders:
            freq_count[r.frequency] = freq_count.get(r.frequency, 0) + 1
        
        return jsonify({
            "success": True,
            "data": {
                "total": len(reminders),
                "active": active_count,
                "inactive": inactive_count,
                "by_frequency": freq_count
            }
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    try:
        app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
    finally:
        reminder_scheduler.stop()
