import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Legacy single-agent risk calculation (keep for backward compatibility)
export const calculateRisk = async (healthData) => {
  const response = await api.post('/risk', healthData);
  return response.data;
};

// NEW: Multi-agent comprehensive risk assessment
export const calculateRiskAggregate = async (healthData) => {
  const response = await api.post('/aggregate', healthData);
  return response.data;
};

export const getHistory = async (userId = null, limit = 10) => {
  const params = {};
  if (userId) params.user_id = userId;
  if (limit) params.limit = limit;
  
  const response = await api.get('/history', { params });
  return response.data;
};

export const getAssessment = async (assessmentId) => {
  const response = await api.get(`/history/${assessmentId}`);
  return response.data;
};

export const deleteAssessment = async (assessmentId) => {
  const response = await api.delete(`/history/${assessmentId}`);
  return response.data;
};

export const getStatistics = async (userId = null) => {
  const params = {};
  if (userId) params.user_id = userId;
  
  const response = await api.get('/statistics', { params });
  return response.data;
};

// NEW: Admin API endpoints
export const getSystemStatus = async () => {
  const response = await api.get('/admin/system/status');
  return response.data;
};

export const getSystemMetrics = async () => {
  const response = await api.get('/admin/system/metrics');
  return response.data;
};

export const getAuditLogs = async (params = {}) => {
  const response = await api.get('/admin/audit-logs', { params });
  return response.data;
};

export const getAuditStats = async (days = 30) => {
  const response = await api.get('/admin/audit-logs/stats', { params: { days } });
  return response.data;
};

export default api;  // <-- MOVED TO THE END