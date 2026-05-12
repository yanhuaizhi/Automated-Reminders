import React from 'react';
import ReminderItem from './ReminderItem';
import './ReminderList.css';

const ReminderList = ({ reminders, onDelete, onToggle }) => {
  if (reminders.length === 0) {
    return (
      <div className="empty-state">
        <p>📭 暂无提醒</p>
        <p className="text-muted">添加你的第一个提醒吧！</p>
      </div>
    );
  }

  return (
    <div className="reminder-list">
      {reminders.map(reminder => (
        <ReminderItem
          key={reminder.id}
          reminder={reminder}
          onDelete={() => onDelete(reminder.id)}
          onToggle={() => onToggle(reminder.id)}
        />
      ))}
    </div>
  );
};

export default ReminderList;
