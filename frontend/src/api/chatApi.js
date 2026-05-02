import axios from 'axios';

// Use environment variable or fallback to localhost for development
let API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Remove trailing slash if present to avoid double slashes like //chat
if (API_BASE_URL.endsWith('/')) {
  API_BASE_URL = API_BASE_URL.slice(0, -1);
}

export const sendChatMessage = async (query) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, { query });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
