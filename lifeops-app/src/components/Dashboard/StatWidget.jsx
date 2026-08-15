import React from 'react';
import './StatWidget.css';

export function StatWidget({ title, value, subtitle, icon: Icon, color = 'emerald', trend }) {
  return (
    <div className={`stat-widget glass-card color-${color}`}>
      <div className="stat-widget-header">
        <span className="stat-title">{title}</span>
        {Icon && (
          <div className="stat-icon-wrapper">
            <Icon size={20} />
          </div>
        )}
      </div>

      <div className="stat-widget-body">
        <span className="stat-value">{value ?? 0}</span>
        {subtitle && <span className="stat-subtitle">{subtitle}</span>}
      </div>

      {trend && (
        <div className="stat-widget-footer">
          <span className={`stat-trend ${trend.positive ? 'up' : 'down'}`}>
            {trend.positive ? '↑' : '↓'} {trend.text}
          </span>
        </div>
      )}
    </div>
  );
}
