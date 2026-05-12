import React, { useState } from 'react';
import './ReminderForm.css';

const ReminderForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    remind_date: '',
    remind_time: '09:00',
    frequency: 'once',
    notification_types: ['system'],
    is_active: true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleNotificationChange = (type) => {
    setFormData(prev => ({
      ...prev,
      notification_types: prev.notification_types.includes(type)
        ? prev.notification_types.filter(t => t !== type)
        : [...prev.notification_types, type]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      alert('请输入提醒标题');
      return;
    }
    onSubmit(formData);
  };

  return (
    <form className="reminder-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="title">标题 *</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="输入提醒标题"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">描述</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="输入提醒描述（可选）"
          rows="3"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="remind_date">日期</label>
          <input
            type="date"
            id="remind_date"
            name="remind_date"
            value={formData.remind_date}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="remind_time">时间 *</label>
          <input
            type="time"
            id="remind_time"
            name="remind_time"
            value={formData.remind_time}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="frequency">频率 *</label>
        <select
          id="frequency"
          name="frequency"
          value={formData.frequency}
          onChange={handleChange}
          required
        >
          <option value="once">一次性</option>
          <option value="daily">每日</option>
          <option value="weekly">每周</option>
          <option value="monthly">每月</option>
        </select>
      </div>

      <div className="form-group">
        <label>通知方式</label>
        <div className="checkboxes">
          <label>
            <input
              type="checkbox"
              checked={formData.notification_types.includes('system')}
              onChange={() => handleNotificationChange('system')}
            />
            系统通知
          </label>
          <label>
            <input
              type="checkbox"
              checked={formData.notification_types.includes('email')}
              onChange={() => handleNotificationChange('email')}
            />
            邮件通知
          </label>
          <label>
            <input
              type="checkbox"
              checked={formData.notification_types.includes('webhook')}
              onChange={() => handleNotificationChange('webhook')}
            />
            Webhook
          </label>
        </div>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="is_active"
            checked={formData.is_active}
            onChange={handleChange}
          />
          启用此提醒
        </label>
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-submit">提交</button>
        <button type="button" className="btn-cancel" onClick={onCancel}>取消</button>
      </div>
    </form>
  );
};

export default ReminderForm;
