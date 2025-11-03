import React, { useState, useEffect } from 'react';
import './StatisticsPanel.css';
import { getStatistics, getHistory } from '../services/api';
import { Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function StatisticsPanel({ refreshTrigger }) {
  const [statistics, setStatistics] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, [refreshTrigger]);

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [stats, historyData] = await Promise.all([
        getStatistics(),
        getHistory(null, 20)
      ]);
      setStatistics(stats);
      setHistory(historyData.assessments);
    } catch (err) {
      setError('Failed to load statistics. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="card">
        <h2>Statistics</h2>
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <h2>Statistics</h2>
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!statistics || statistics.total_assessments === 0) {
    return (
      <div className="card">
        <h2>Statistics</h2>
        <div className="empty-state">
          <p>📊 No statistics available</p>
          <p className="empty-subtitle">Complete assessments to see statistics</p>
        </div>
      </div>
    );
  }

  // Pie chart for risk distribution
  const pieData = {
    labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
    datasets: [{
      data: [
        statistics.low_risk_count,
        statistics.moderate_risk_count,
        statistics.high_risk_count
      ],
      backgroundColor: [
        'rgba(72, 187, 120, 0.8)',
        'rgba(237, 137, 54, 0.8)',
        'rgba(245, 101, 101, 0.8)'
      ],
      borderColor: [
        'rgb(72, 187, 120)',
        'rgb(237, 137, 54)',
        'rgb(245, 101, 101)'
      ],
      borderWidth: 2
    }]
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  };

  // Line chart for risk score trends
  const sortedHistory = [...history].reverse();
  const lineData = {
    labels: sortedHistory.map((_, index) => `#${index + 1}`),
    datasets: [{
      label: 'Risk Score Over Time',
      data: sortedHistory.map(item => item.overall_score),
      borderColor: 'rgb(102, 126, 234)',
      backgroundColor: 'rgba(102, 126, 234, 0.1)',
      tension: 0.4,
      fill: true
    }]
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        }
      }
    }
  };

  return (
    <div className="statistics-panel">
      <div className="card">
        <div className="stats-header">
          <h2>Statistics Overview</h2>
          <button onClick={loadData} className="secondary refresh-btn">
            🔄 Refresh
          </button>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-value">{statistics.total_assessments}</div>
            <div className="stat-label">Total Assessments</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-value">{statistics.avg_risk_score}</div>
            <div className="stat-label">Average Risk Score</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📏</div>
            <div className="stat-value">{statistics.avg_bmi}</div>
            <div className="stat-label">Average BMI</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-value">{statistics.low_risk_count}</div>
            <div className="stat-label">Low Risk</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⚠️</div>
            <div className="stat-value">{statistics.moderate_risk_count}</div>
            <div className="stat-label">Moderate Risk</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🚨</div>
            <div className="stat-value">{statistics.high_risk_count}</div>
            <div className="stat-label">High Risk</div>
          </div>
        </div>

        <div className="charts-grid">
          <div className="chart-card">
            <h3>Risk Level Distribution</h3>
            <div className="chart-container-pie">
              <Pie data={pieData} options={pieOptions} />
            </div>
          </div>

          <div className="chart-card">
            <h3>Risk Score Trend</h3>
            <div className="chart-container-line">
              <Line data={lineData} options={lineOptions} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StatisticsPanel;
