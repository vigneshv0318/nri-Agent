import api from './api';

export const userService = {
  async getProfile() {
    const response = await api.get('/user/profile');
    return response.data;
  },

  async updateLanguage(language) {
    const response = await api.put('/user/language', { language });
    return response.data;
  },

  async getStamps() {
    const response = await api.get('/user/stamps');
    return response.data;
  }
};
