import React from 'react';
import './Statistics.css';

const Statistics = ({ stats }) => {
  return (
    <div className="statistics">
      <div className="stat-card">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <span className="stat-label">总计</span>
          <span className="stat-value">{stats.total || 0}</span>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">✓</div>
        <div className="stat-content">
          <span className="stat-label">启用中</span>
          <span className="stat-value">{stats.active || 0}</span>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">○</div>
        <div className="stat-content">
          <span className="stat-label">已禁用</span>
          <span className="stat-value">{stats.inactive || 0}</span>
        </div>
      </div>

      {stats.by_frequency && (
        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-content">
            <span className="stat-label">频率分布</span>
            <span className="stat-frequency">
              {Object.entries(stats.by_frequency).map(([freq, count]) => (
                <span key={freq}>{freq}: {count}</span>
              ))}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Statistics;
