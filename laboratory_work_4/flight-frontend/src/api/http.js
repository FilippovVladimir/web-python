import axios from "axios";

const apiBase = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const http = axios.create({
  baseURL: apiBase,
  timeout: 10000,
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("auth_token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});
