import React from 'react';
import './RiskResult.css';
import { Doughnut, Bar, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register ChartJS components including Radar
ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Title,
  Tooltip,
  Legend
);

function RiskResult({ result, onReset }) {
  // Extract data from multi-agent response
  const overallScore = result.overall_health_index || 0;
  const riskLevel = result.overall_risk_level || 'Unknown';
  const agentAssessments = result.agent_assessments || {};
  const recommendations = result.integrated_recommendations || [];
  const criticalAreas = result.critical_areas || [];
  
  // Extract BMI from metabolic agent if available
  const bmi = agentAssessments.metabolic?.bmi || null;
  const bmiClassification = agentAssessments.metabolic?.details?.bmi_classification || '';

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

  const getAgentIcon = (agentKey) => {
    switch (agentKey) {
      case 'cardio':
        return '❤️';
      case 'metabolic':
        return '⚡';
      case 'neuro':
        return '🧠';
      default:
        return '📊';
    }
  };

  // Doughnut chart data for overall score
  const doughnutData = {
    labels: ['Risk Score', 'Remaining'],
    datasets: [{
      data: [overallScore, 100 - overallScore],
      backgroundColor: [
        getRiskColor(riskLevel),
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

  // Radar chart data for agent comparison
  const agentKeys = Object.keys(agentAssessments);
  const agentLabels = agentKeys.map(key => 
    agentAssessments[key].category || key.charAt(0).toUpperCase() + key.slice(1)
  );
  const agentScores = agentKeys.map(key => agentAssessments[key].risk_score || 0);

  const radarData = {
    labels: agentLabels,
    datasets: [{
      label: 'Risk Scores',
      data: agentScores,
      backgroundColor: 'rgba(102, 126, 234, 0.2)',
      borderColor: 'rgb(102, 126, 234)',
      borderWidth: 2,
      pointBackgroundColor: 'rgb(102, 126, 234)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(102, 126, 234)',
      pointRadius: 5,
      pointHoverRadius: 7
    }]
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 20
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        angleLines: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return context.label + ': ' + context.parsed.r.toFixed(1) + '/100';
          }
        }
      }
    }
  };

  // Bar chart data for agent comparison
  const barData = {
    labels: agentLabels,
    datasets: [{
      label: 'Agent Risk Scores',
      data: agentScores,
      backgroundColor: [
        'rgba(237, 100, 166, 0.7)',
        'rgba(102, 126, 234, 0.7)',
        'rgba(118, 75, 162, 0.7)'
      ],
      borderColor: [
        'rgb(237, 100, 166)',
        'rgb(102, 126, 234)',
        'rgb(118, 75, 162)'
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
        max: 100
      }
    }
  };

  return (
    <div className="risk-result">
      <div className="result-header">
        <div className="success">✓ Multi-Agent Risk Assessment Complete</div>
        {criticalAreas.length > 0 && (
          <div className="critical-warning">
            ⚠️ Critical Areas: {criticalAreas.join(', ')}
          </div>
        )}
      </div>

      <div className="result-grid">
        <div className="result-card overall-score">
          <h3>Overall Health Index</h3>
          <div className="score-visual">
            <div className="doughnut-container">
              <Doughnut data={doughnutData} options={doughnutOptions} />
              <div className="score-center">
                <div className="score-value">{overallScore.toFixed(1)}</div>
                <div className="score-label">/ 100</div>
              </div>
            </div>
          </div>
          <div className="risk-badge" style={{ backgroundColor: getRiskColor(riskLevel) }}>
            {getRiskIcon(riskLevel)} {riskLevel} Risk
          </div>
        </div>

        {bmi && (
          <div className="result-card bmi-info">
            <h3>Body Mass Index (BMI)</h3>
            <div className="bmi-value">{bmi.toFixed(1)}</div>
            <div className="bmi-classification">{bmiClassification}</div>
            <div className="bmi-categories">
              <div className={bmi < 18.5 ? 'active' : ''}>
                Underweight {'(<18.5)'}
              </div>
              <div className={bmi >= 18.5 && bmi < 25 ? 'active' : ''}>
                Normal (18.5-24.9)
              </div>
              <div className={bmi >= 25 && bmi < 30 ? 'active' : ''}>
                Overweight (25-29.9)
              </div>
              <div className={bmi >= 30 ? 'active' : ''}>
                Obese {'(≥30)'}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* NEW: Radar chart for visual agent comparison */}
      <div className="result-card radar-chart">
        <h3>Multi-Domain Health Profile</h3>
        <div className="chart-container radar-container">
          <Radar data={radarData} options={radarOptions} />
        </div>
        <div className="breakdown-legend">
          <p>Visual comparison of risk across all health domains. Lower scores indicate better health.</p>
        </div>
      </div>

      {/* Agent-specific result cards */}
      <div className="agent-cards">
        {agentKeys.map(agentKey => {
          const agent = agentAssessments[agentKey];
          return (
            <div key={agentKey} className="result-card agent-card">
              <div className="agent-header">
                <h3>
                  {getAgentIcon(agentKey)} {agent.category}
                </h3>
                <div 
                  className="agent-risk-badge"
                  style={{ backgroundColor: getRiskColor(agent.risk_level) }}
                >
                  {agent.risk_level}
                </div>
              </div>
              <div className="agent-score">{agent.risk_score.toFixed(1)} / 100</div>
              
              {/* NEW: Show breakdown of risk factors for this agent */}
              {agent.breakdown && (
                <div className="agent-breakdown">
                  <h4>Risk Factors:</h4>
                  <div className="breakdown-items">
                    {Object.entries(agent.breakdown).map(([factor, value]) => (
                      <div key={factor} className="breakdown-item">
                        <span className="factor-name">
                          {factor.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                        <div className="factor-bar">
                          <div 
                            className="factor-fill" 
                            style={{ 
                              width: `${value}%`,
                              backgroundColor: value > 50 ? '#f56565' : value > 30 ? '#ed8936' : '#48bb78'
                            }}
                          />
                        </div>
                        <span className="factor-value">{value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {agent.recommendations && agent.recommendations.length > 0 && (
                <div className="agent-recommendations">
                  <h4>Recommendations:</h4>
                  <ul>
                    {agent.recommendations.slice(0, 3).map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="result-card breakdown">
        <h3>Agent Risk Comparison</h3>
        <div className="chart-container">
          <Bar data={barData} options={barOptions} />
        </div>
        <div className="breakdown-legend">
          <p>Lower scores indicate better health in each domain.</p>
        </div>
      </div>

      {recommendations.length > 0 && (
        <div className="result-card recommendations">
          <h3>Integrated Health Recommendations</h3>
          <ul className="recommendation-list">
            {recommendations.slice(0, 8).map((rec, idx) => (
              <li key={idx}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="result-actions">
        <button onClick={onReset} className="primary">
          Calculate Another Assessment
        </button>
      </div>
    </div>
  );
}

export default RiskResult;