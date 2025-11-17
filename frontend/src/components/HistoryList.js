import React, { useState, useEffect } from 'react';
import './HistoryList.css';
import { getHistory, deleteAssessment } from '../services/api';

function HistoryList({ refreshTrigger }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, [refreshTrigger]);

  const loadHistory = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getHistory(null, 20);
      setHistory(data.assessments);
    } catch (err) {
      setError('Failed to load history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (assessmentId) => {
    if (!window.confirm('Are you sure you want to delete this assessment?')) {
      return;
    }

    try {
      await deleteAssessment(assessmentId);
      setHistory(prev => prev.filter(item => item.id !== assessmentId));
    } catch (err) {
      alert('Failed to delete assessment. Please try again.');
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'Low':
        return '#48bb78';
      case 'Moderate':
        return '#ed8936';
      case 'High':
        return '#f56565';
      default:
        return '#718096';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="card">
        <h2>Assessment History</h2>
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="history-list">
      <div className="card">
        <div className="history-header">
          <h2>Assessment History</h2>
          <button onClick={loadHistory} className="secondary refresh-btn">
            🔄 Refresh
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        {history.length === 0 ? (
          <div className="empty-state">
            <p>📋 No assessments found</p>
            <p className="empty-subtitle">Complete a risk assessment to see it here</p>
          </div>
        ) : (
          <div className="history-items">
            {history.map((item) => (
              <div key={item.id} className="history-item">
                <div className="item-header">
                  <div className="item-date">{formatDate(item.created_at)}</div>
                  <div 
                    className="item-risk-badge"
                    style={{ backgroundColor: getRiskColor(item.risk_level) }}
                  >
                    {item.risk_level} Risk
                  </div>
                </div>

                <div className="item-body">
                  <div className="item-score">
                    <div className="score-label">Overall Score</div>
                    <div className="score-value">{item.overall_score}</div>
                  </div>

                  <div className="item-details">
                    <div className="detail-row">
                      <span className="detail-label">Age:</span>
                      <span className="detail-value">{item.age} years</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">BMI:</span>
                      <span className="detail-value">{item.bmi}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Blood Pressure:</span>
                      <span className="detail-value">{item.systolic}/{item.diastolic}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Cholesterol:</span>
                      <span className="detail-value">{item.cholesterol} mg/dL</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Smoker:</span>
                      <span className="detail-value">{item.is_smoker ? 'Yes' : 'No'}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Exercise:</span>
                      <span className="detail-value">{item.exercise_days} days/week</span>
                    </div>
                  </div>
                </div>

                <div className="item-actions">
                  <button 
                    onClick={() => handleDelete(item.id)}
                    className="danger delete-btn"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default HistoryList;
