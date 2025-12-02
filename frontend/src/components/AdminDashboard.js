import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';
import { getSystemStatus, getSystemMetrics, getAuditLogs } from '../services/api';

function AdminDashboard() {
  const [systemStatus, setSystemStatus] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError('');
    
    try {
      const [statusData, metricsData, logsData] = await Promise.all([
        getSystemStatus(),
        getSystemMetrics(),
        getAuditLogs({ limit: 20 })
      ]);

      setSystemStatus(statusData);
      setMetrics(metricsData);
      setAuditLogs(logsData.logs || []);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="loading">Loading admin dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h2>🔧 Admin Dashboard</h2>
        <button onClick={loadDashboardData} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {/* System Status */}
      <div className="status-section">
        <div className="status-card healthy">
          <div className="status-icon">✓</div>
          <div className="status-info">
            <h3>System Status</h3>
            <p>{systemStatus?.status || 'Unknown'}</p>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-value">{metrics?.total_assessments || 0}</div>
          <div className="metric-label">Total Assessments</div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">⚡</div>
          <div className="metric-value">{metrics?.average_risk_score || 0}</div>
          <div className="metric-label">Average Risk Score</div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📏</div>
          <div className="metric-value">{metrics?.average_bmi || 0}</div>
          <div className="metric-label">Average BMI</div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">🚀</div>
          <div className="metric-value">{metrics?.performance?.avg_response_time_ms || 'N/A'}</div>
          <div className="metric-label">Avg Response Time</div>
        </div>
      </div>

      {/* Risk Distribution */}
      {metrics?.risk_distribution && (
        <div className="card">
          <h3>Risk Distribution</h3>
          <div className="risk-distribution">
            <div className="risk-item low">
              <div className="risk-bar" style={{ width: `${metrics.risk_distribution.low.percentage}%` }}></div>
              <div className="risk-info">
                <span className="risk-label">Low Risk</span>
                <span className="risk-count">{metrics.risk_distribution.low.count} ({metrics.risk_distribution.low.percentage}%)</span>
              </div>
            </div>
            <div className="risk-item moderate">
              <div className="risk-bar" style={{ width: `${metrics.risk_distribution.moderate.percentage}%` }}></div>
              <div className="risk-info">
                <span className="risk-label">Moderate Risk</span>
                <span className="risk-count">{metrics.risk_distribution.moderate.count} ({metrics.risk_distribution.moderate.percentage}%)</span>
              </div>
            </div>
            <div className="risk-item high">
              <div className="risk-bar" style={{ width: `${metrics.risk_distribution.high.percentage}%` }}></div>
              <div className="risk-info">
                <span className="risk-label">High Risk</span>
                <span className="risk-count">{metrics.risk_distribution.high.count} ({metrics.risk_distribution.high.percentage}%)</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Audit Logs */}
      <div className="card">
        <h3>Recent Activity (Audit Logs)</h3>
        {auditLogs.length === 0 ? (
          <p className="no-logs">No audit logs available</p>
        ) : (
          <div className="audit-logs-table">
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Action</th>
                  <th>Resource</th>
                  <th>Status</th>
                  <th>User ID</th>
                </tr>
              </thead>
              <tbody>
                {auditLogs.map((log, index) => (
                  <tr key={index}>
                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                    <td><span className="action-badge">{log.action}</span></td>
                    <td>{log.resource}</td>
                    <td>
                      <span className={`status-badge ${log.status}`}>
                        {log.status}
                      </span>
                    </td>
                    <td>{log.user_id || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;