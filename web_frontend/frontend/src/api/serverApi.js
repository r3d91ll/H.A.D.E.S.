import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

export const serverApi = {
  listServers: async () => {
    const response = await axios.get(`${API_BASE_URL}/servers/list`);
    return response.data;
  },

  startServer: async (config) => {
    const response = await axios.post(`${API_BASE_URL}/servers/start`, config);
    return response.data;
  },

  stopServer: async (serverId) => {
    const response = await axios.post(`${API_BASE_URL}/servers/stop/${serverId}`);
    return response.data;
  },

  checkHealth: async (serverId) => {
    const response = await axios.get(`${API_BASE_URL}/servers/health/${serverId}`);
    return response.data;
  },
};
