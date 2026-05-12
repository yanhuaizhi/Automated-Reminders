import React from 'react';
import './ReminderItem.css';

const ReminderItem = ({ reminder, onDelete, onToggle }) => {
  const getFrequencyLabel = (frequency) => {
    const labels = {
      once: '一次性',
      daily: '每日',
      weekly: '每周',
      monthly: '每月'
    };
    return labels[frequency] || frequency;
  };

  return (
    <div className={`reminder-item ${!reminder.is_active ? 'inactive' : ''}`}>
      <div className="reminder-header">
        <h3>{reminder.title}</h3>
        <span className="frequency-badge">{getFrequencyLabel(reminder.frequency)}</span>
      </div>

      {reminder.description && (
        <p className="description">{reminder.description}</p>
      )}

      <div className="reminder-meta">
        <div className="meta-item">
          <span className="label">⏰ 时间:</span>
          <span>{reminder.remind_time}</span>
        </div>
        {reminder.remind_date && (
          <div className="meta-item">
            <span className="label">📅 日期:</span>
            <span>{reminder.remind_date}</span>
          </div>
        )}
      </div>

      <div className="notification-types">
        {reminder.notification_types.map(type => (
          <span key={type} className="notification-badge">
            {type === 'system' ? '🔔' : type === 'email' ? '📧' : '🔗'}
            {type}
          </span>
        ))}
      </div>

      <div className="reminder-actions">
        <button
          className="btn-toggle"
          onClick={onToggle}
          title={reminder.is_active ? '禁用' : '启用'}
        >
          {reminder.is_active ? '✓ 启用' : '○ 禁用'}
        </button>
        <button
          className="btn-delete"
          onClick={onDelete}
          title="删除"
        >
          🗑️ 删除
        </button>
      </div>
    </div>
  );
};

export default ReminderItem;
