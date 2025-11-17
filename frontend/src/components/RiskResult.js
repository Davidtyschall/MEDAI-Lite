import React from 'react';
import './RiskResult.css';
import { Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function RiskResult({ result, onReset }) {
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

  const getRiskIcon = (level) => {
    switch (level) {
      case 'Low':
        return '✅';
      case 'Moderate':
        return '⚠️';
      case 'High':
        return '🚨';
      default:
        return 'ℹ️';
    }
  };

  // Doughnut chart data for overall score
  const doughnutData = {
    labels: ['Risk Score', 'Remaining'],
    datasets: [{
      data: [result.overall_score, 100 - result.overall_score],
      backgroundColor: [
        getRiskColor(result.risk_level),
        '#e2e8f0'
      ],
      borderWidth: 0
    }]
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: true
      }
    },
    cutout: '75%'
  };

  // Bar chart data for breakdown
  const breakdownData = {
    labels: ['Age', 'BMI', 'Blood Pressure', 'Cholesterol', 'Smoking', 'Exercise'],
    datasets: [{
      label: 'Risk Factors',
      data: [
        result.breakdown.age,
        result.breakdown.bmi,
        result.breakdown.blood_pressure,
        result.breakdown.cholesterol,
        result.breakdown.smoking,
        result.breakdown.exercise
      ],
      backgroundColor: [
        'rgba(102, 126, 234, 0.7)',
        'rgba(118, 75, 162, 0.7)',
        'rgba(237, 100, 166, 0.7)',
        'rgba(255, 154, 158, 0.7)',
        'rgba(255, 183, 77, 0.7)',
        'rgba(129, 199, 132, 0.7)'
      ],
      borderColor: [
        'rgb(102, 126, 234)',
        'rgb(118, 75, 162)',
        'rgb(237, 100, 166)',
        'rgb(255, 154, 158)',
        'rgb(255, 183, 77)',
        'rgb(129, 199, 132)'
      ],
      borderWidth: 2
    }]
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: false
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
    <div className="risk-result">
      <div className="result-header">
        <div className="success">✓ Risk Assessment Complete</div>
      </div>

      <div className="result-grid">
        <div className="result-card overall-score">
          <h3>Overall Risk Score</h3>
          <div className="score-visual">
            <div className="doughnut-container">
              <Doughnut data={doughnutData} options={doughnutOptions} />
              <div className="score-center">
                <div className="score-value">{result.overall_score}</div>
                <div className="score-label">/ 100</div>
              </div>
            </div>
          </div>
          <div className="risk-badge" style={{ backgroundColor: getRiskColor(result.risk_level) }}>
            {getRiskIcon(result.risk_level)} {result.risk_level} Risk
          </div>
        </div>

        <div className="result-card bmi-info">
          <h3>Body Mass Index (BMI)</h3>
          <div className="bmi-value">{result.bmi}</div>
          <div className="bmi-categories">
            <div className={result.bmi < 18.5 ? 'active' : ''}>
              Underweight {'(<18.5)'}
            </div>
            <div className={result.bmi >= 18.5 && result.bmi < 25 ? 'active' : ''}>
              Normal (18.5-24.9)
            </div>
            <div className={result.bmi >= 25 && result.bmi < 30 ? 'active' : ''}>
              Overweight (25-29.9)
            </div>
            <div className={result.bmi >= 30 ? 'active' : ''}>
              Obese {'(≥30)'}
            </div>
          </div>
        </div>
      </div>

      <div className="result-card breakdown">
        <h3>Risk Factor Breakdown</h3>
        <div className="chart-container">
          <Bar data={breakdownData} options={barOptions} />
        </div>
        <div className="breakdown-legend">
          <p>Higher scores indicate greater risk contribution from each factor.</p>
        </div>
      </div>

      <div className="result-actions">
        <button onClick={onReset} className="primary">
          Calculate Another Assessment
        </button>
      </div>
    </div>
  );
}

export default RiskResult;
