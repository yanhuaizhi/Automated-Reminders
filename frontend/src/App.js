import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReminderList from './components/ReminderList';
import ReminderForm from './components/ReminderForm';
import Statistics from './components/Statistics';
import './App.css';

const API_BASE = '/api';

function App() {
  const [reminders, setReminders] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadReminders();
    loadStatistics();
  }, []);

  const loadReminders = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/reminders`);
      setReminders(response.data.data);
    } catch (error) {
      console.error('Error loading reminders:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const response = await axios.get(`${API_BASE}/statistics`);
      setStats(response.data.data);
    } catch (error) {
      console.error('Error loading statistics:', error);
    }
  };

  const handleAddReminder = async (reminderData) => {
    try {
      const response = await axios.post(`${API_BASE}/reminders`, reminderData);
      setReminders([...reminders, response.data.data]);
      setShowForm(false);
      loadStatistics();
    } catch (error) {
      console.error('Error adding reminder:', error);
    }
  };

  const handleDeleteReminder = async (reminderId) => {
    try {
      await axios.delete(`${API_BASE}/reminders/${reminderId}`);
      setReminders(reminders.filter(r => r.id !== reminderId));
      loadStatistics();
    } catch (error) {
      console.error('Error deleting reminder:', error);
    }
  };

  const handleToggleReminder = async (reminderId) => {
    try {
      const response = await axios.post(`${API_BASE}/reminders/${reminderId}/toggle`);
      setReminders(reminders.map(r => r.id === reminderId ? response.data.data : r));
      loadStatistics();
    } catch (error) {
      console.error('Error toggling reminder:', error);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔔 Automated Reminders</h1>
        <p>Never forget what you should do</p>
      </header>

      <main className="app-main">
        <Statistics stats={stats} />

        <button
          className="btn-add"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? '✕ 关闭' : '+ 添加提醒'}
        </button>

        {showForm && (
          <ReminderForm
            onSubmit={handleAddReminder}
            onCancel={() => setShowForm(false)}
          />
        )}

        {loading ? (
          <div className="loading">加载中...</div>
        ) : (
          <ReminderList
            reminders={reminders}
            onDelete={handleDeleteReminder}
            onToggle={handleToggleReminder}
          />
        )}
      </main>
    </div>
  );
}

export default App;
