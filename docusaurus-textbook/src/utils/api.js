/**
 * Axios configuration for API calls.
 * 
 * Provides configured axios instance with interceptors.
 */

import axios from 'axios';

// Webpack 5 does not polyfill process. Using hardcoded dev URL.
const API_BASE_URL = 'https://mb-murad-physical-ai-backend.hf.space';

/**
 * Create axios instance with default configuration
 */
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Request interceptor to add auth token
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor to handle auth errors
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear storage and redirect
      localStorage.removeItem('access_token');
      window.location.href = '/physical-ai-humanoid-robotics-textbook/';
    }
    return Promise.reject(error);
  }
);

export default api;
