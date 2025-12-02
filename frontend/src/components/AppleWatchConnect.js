import React, { useState } from 'react';
import './AppleWatchConnect.css';

function AppleWatchConnect({ onDataImport }) {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [sessionKey, setSessionKey] = useState(null);
  const [deviceInfo, setDeviceInfo] = useState(null);
  const [healthData, setHealthData] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');

  const handleConnect = async () => {
    setConnecting(true);
    setError('');

    try {
      // Connect to Apple Watch
      const connectResponse = await fetch('/api/watch/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1 })
      });

      if (!connectResponse.ok) {
        throw new Error('Failed to connect to Apple Watch');
      }

      const connectData = await connectResponse.json();
      setConnected(true);
      setSessionKey(connectData.session_key);
      setDeviceInfo(connectData.device);

      // Fetch sample health data
      const dataResponse = await fetch('/api/watch/sample-data');
      
      if (!dataResponse.ok) {
        throw new Error('Failed to fetch health data');
      }

      const data = await dataResponse.json();
      setHealthData(data.data);
      setShowModal(true);

    } catch (err) {
      setError(err.message || 'Failed to connect to Apple Watch');
      setConnected(false);
    } finally {
      setConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    try {
      await fetch('/api/watch/disconnect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_key: sessionKey })
      });

      setConnected(false);
      setSessionKey(null);
      setDeviceInfo(null);
      setHealthData(null);
      setShowModal(false);
    } catch (err) {
      setError('Failed to disconnect');
    }
  };

  const handleImportData = () => {
    if (healthData && onDataImport) {
      onDataImport(healthData);
      setShowModal(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="apple-watch-connect">
      <div className="watch-status">
        {!connected ? (
          <button 
            onClick={handleConnect} 
            className="connect-button"
            disabled={connecting}
          >
            {connecting ? (
              <>
                <span className="spinner"></span> Connecting...
              </>
            ) : (
              <>
                ⌚ Connect Apple Watch
              </>
            )}
          </button>
        ) : (
          <div className="connected-status">
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span className="status-text">
                Apple Watch Connected
                {deviceInfo && <span className="device-model"> • {deviceInfo.model}</span>}
              </span>
            </div>
            <button onClick={handleDisconnect} className="disconnect-button">
              Disconnect
            </button>
          </div>
        )}
      </div>

      {error && <div className="watch-error">{error}</div>}

      {/* Data Import Modal */}
      {showModal && healthData && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>⌚ Apple Watch Data Found</h3>
              <button className="close-button" onClick={handleCloseModal}>×</button>
            </div>

            <div className="modal-body">
              <p className="modal-description">
                We've retrieved your health data from your Apple Watch. Review the data below and import it to auto-fill the risk assessment form.
              </p>

              <div className="data-preview">
                <div className="data-grid">
                  <div className="data-item">
                    <span className="data-label">Age</span>
                    <span className="data-value">{healthData.age} years</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Weight</span>
                    <span className="data-value">{healthData.weight_kg} kg</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Height</span>
                    <span className="data-value">{healthData.height_cm} cm</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Blood Pressure</span>
                    <span className="data-value">{healthData.systolic}/{healthData.diastolic} mmHg</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Cholesterol</span>
                    <span className="data-value">{healthData.cholesterol} mg/dL</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Exercise</span>
                    <span className="data-value">{healthData.exercise_days} days/week</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Smoker</span>
                    <span className="data-value">{healthData.is_smoker ? 'Yes' : 'No'}</span>
                  </div>
                  <div className="data-item">
                    <span className="data-label">Data Source</span>
                    <span className="data-value">Apple Watch</span>
                  </div>
                </div>
              </div>

              <div className="modal-info">
                <span className="info-icon">ℹ️</span>
                <span>This data will automatically populate the health risk assessment form.</span>
              </div>
            </div>

            <div className="modal-footer">
              <button onClick={handleCloseModal} className="cancel-button">
                Cancel
              </button>
              <button onClick={handleImportData} className="import-button">
                Import Data
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AppleWatchConnect;