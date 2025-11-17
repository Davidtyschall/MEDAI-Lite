import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import RiskCalculator from '../components/RiskCalculator';
import HistoryList from '../components/HistoryList';
import StatisticsPanel from '../components/StatisticsPanel';
import { healthCheck } from '../services/api';

function Dashboard({ onLogout }) {
  const [activeTab, setActiveTab] = useState('calculator');
  const [apiStatus, setApiStatus] = useState('checking');
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const username = localStorage.getItem('medai_user') || 'Guest';

  useEffect(() => {
    checkAPIHealth();
  }, []);

  const checkAPIHealth = async () => {
    try {
      await healthCheck();
      setApiStatus('healthy');
    } catch (error) {
      setApiStatus('error');
    }
  };

  const handleCalculationComplete = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo-small">
              <svg width="32" height="32" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="22" stroke="white" strokeWidth="3"/>
                <path d="M24 12v24M12 24h24" stroke="white" strokeWidth="3" strokeLinecap="round"/>
              </svg>
            </div>
            <h1>MEDAI-Lite</h1>
          </div>
          <div className="header-right">
            <div className="user-info">
              <span className="username">👤 {username}</span>
              <div className={`api-status ${apiStatus}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                  {apiStatus === 'healthy' ? 'API Connected' : 
                   apiStatus === 'error' ? 'API Error' : 'Checking...'}
                </span>
              </div>
            </div>
            <button onClick={onLogout} className="secondary logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="dashboard-container">
        <nav className="dashboard-nav">
          <button 
            className={activeTab === 'calculator' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setActiveTab('calculator')}
          >
            📊 Risk Calculator
          </button>
          <button 
            className={activeTab === 'history' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setActiveTab('history')}
          >
            📋 History
          </button>
          <button 
            className={activeTab === 'statistics' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setActiveTab('statistics')}
          >
            📈 Statistics
          </button>
        </nav>

        <main className="dashboard-content">
          {activeTab === 'calculator' && (
            <RiskCalculator onComplete={handleCalculationComplete} />
          )}
          {activeTab === 'history' && (
            <HistoryList refreshTrigger={refreshTrigger} />
          )}
          {activeTab === 'statistics' && (
            <StatisticsPanel refreshTrigger={refreshTrigger} />
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
