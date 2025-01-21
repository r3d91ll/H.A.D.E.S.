import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

export const modelApi = {
  listModels: async () => {
    const response = await axios.get(`${API_BASE_URL}/models/list`);
    return response.data;
  },

  downloadModel: async (modelName) => {
    const response = await axios.post(`${API_BASE_URL}/models/download`, { model_name: modelName });
    return response.data;
  },

  loadModel: async (modelName, gpuId = null) => {
    const response = await axios.post(`${API_BASE_URL}/models/load`, {
      model_name: modelName,
      gpu_id: gpuId,
    });
    return response.data;
  },

  unloadModel: async (modelName) => {
    const response = await axios.post(`${API_BASE_URL}/models/unload`, { model_name: modelName });
    return response.data;
  },
};
