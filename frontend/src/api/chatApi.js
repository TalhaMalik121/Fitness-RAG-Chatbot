import axios from 'axios';

// Use environment variable or fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const sendChatMessage = async (query) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { query });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
