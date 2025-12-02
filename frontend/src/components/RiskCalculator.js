import React, { useState } from 'react';
import './RiskCalculator.css';
import { calculateRiskAggregate } from '../services/api';
import RiskResult from './RiskResult';
import AppleWatchConnect from './AppleWatchConnect';

function RiskCalculator({ onComplete }) {
  const [formData, setFormData] = useState({
    age: '',
    weight_kg: '',
    height_cm: '',
    systolic: '',
    diastolic: '',
    cholesterol: '',
    is_smoker: false,
    exercise_days: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  // NEW: Handle data import from Apple Watch
  const handleWatchDataImport = (watchData) => {
    setFormData({
      age: watchData.age.toString(),
      weight_kg: watchData.weight_kg.toString(),
      height_cm: watchData.height_cm.toString(),
      systolic: watchData.systolic.toString(),
      diastolic: watchData.diastolic.toString(),
      cholesterol: watchData.cholesterol.toString(),
      is_smoker: watchData.is_smoker,
      exercise_days: watchData.exercise_days.toString()
    });
    
    // Show success feedback
    setError('');
    setTimeout(() => {
      const successMsg = document.createElement('div');
      successMsg.className = 'success-toast';
      successMsg.textContent = '✓ Apple Watch data imported successfully!';
      document.body.appendChild(successMsg);
      setTimeout(() => successMsg.remove(), 3000);
    }, 100);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Convert string values to numbers
      const requestData = {
        age: parseInt(formData.age),
        weight_kg: parseFloat(formData.weight_kg),
        height_cm: parseFloat(formData.height_cm),
        systolic: parseInt(formData.systolic),
        diastolic: parseInt(formData.diastolic),
        cholesterol: parseInt(formData.cholesterol),
        is_smoker: formData.is_smoker,
        exercise_days: parseInt(formData.exercise_days)
      };

      // Use multi-agent aggregate endpoint
      const response = await calculateRiskAggregate(requestData);
      setResult(response);
      if (onComplete) onComplete();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to calculate risk. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      age: '',
      weight_kg: '',
      height_cm: '',
      systolic: '',
      diastolic: '',
      cholesterol: '',
      is_smoker: false,
      exercise_days: ''
    });
    setResult(null);
    setError('');
  };

  return (
    <div className="risk-calculator">
      <div className="card">
        <h2>Health Risk Calculator</h2>
        <p className="subtitle">Enter your health information to calculate your risk score</p>

        {/* NEW: Apple Watch Connection */}
        {!result && (
          <AppleWatchConnect onDataImport={handleWatchDataImport} />
        )}

        {error && <div className="error">{error}</div>}

        {!result ? (
          <form onSubmit={handleSubmit} className="calculator-form">
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="age">Age (years) *</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  min="1"
                  max="150"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="weight_kg">Weight (kg) *</label>
                <input
                  type="number"
                  id="weight_kg"
                  name="weight_kg"
                  value={formData.weight_kg}
                  onChange={handleChange}
                  min="20"
                  max="500"
                  step="0.1"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="height_cm">Height (cm) *</label>
                <input
                  type="number"
                  id="height_cm"
                  name="height_cm"
                  value={formData.height_cm}
                  onChange={handleChange}
                  min="50"
                  max="300"
                  step="0.1"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="systolic">Systolic BP (mmHg) *</label>
                <input
                  type="number"
                  id="systolic"
                  name="systolic"
                  value={formData.systolic}
                  onChange={handleChange}
                  min="50"
                  max="250"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="diastolic">Diastolic BP (mmHg) *</label>
                <input
                  type="number"
                  id="diastolic"
                  name="diastolic"
                  value={formData.diastolic}
                  onChange={handleChange}
                  min="30"
                  max="150"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="cholesterol">Total Cholesterol (mg/dL) *</label>
                <input
                  type="number"
                  id="cholesterol"
                  name="cholesterol"
                  value={formData.cholesterol}
                  onChange={handleChange}
                  min="100"
                  max="400"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="exercise_days">Exercise Days/Week *</label>
                <select
                  id="exercise_days"
                  name="exercise_days"
                  value={formData.exercise_days}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select...</option>
                  <option value="0">0 days</option>
                  <option value="1">1 day</option>
                  <option value="2">2 days</option>
                  <option value="3">3 days</option>
                  <option value="4">4 days</option>
                  <option value="5">5 days</option>
                  <option value="6">6 days</option>
                  <option value="7">7 days</option>
                </select>
              </div>

              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="is_smoker"
                    checked={formData.is_smoker}
                    onChange={handleChange}
                  />
                  <span>I am a smoker</span>
                </label>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="primary" disabled={loading}>
                {loading ? 'Calculating...' : 'Calculate Risk'}
              </button>
            </div>
          </form>
        ) : (
          <RiskResult result={result} onReset={handleReset} />
        )}
      </div>
    </div>
  );
}

export default RiskCalculator;