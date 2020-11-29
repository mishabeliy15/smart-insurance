import axios from "axios";
import history from "./history";

const API_URL = process.env.API_URL || "http://localhost/api/v0/";

const api = axios.create({ baseURL: API_URL });

// Add a request interceptor

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers["Authorization"] = "Bearer " + token;
    }
    const lang = localStorage.getItem("i18nextLng");
    if (lang) {
      config.headers["Accept-Language"] = lang;
    }
    config.headers["Content-Type"] = "application/json";
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

//Add a response interceptor

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const originalRequest = error.config;

    if (
      error.response.status === 401 &&
      originalRequest.url === `${API_URL}auth/jwt/refresh/`
    ) {
      history.push("/login");
      return Promise.reject(error);
    }

    if (originalRequest.url.includes("/auth/")) return Promise.reject(error);

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh");
      return api
        .post("auth/jwt/refresh/", {
          refresh: refreshToken,
        })
        .then((res) => {
          if (res.status === 200) {
            localStorage.setItem("access", res.data.access);
            // localStorage.setItem("refresh", res.data.refresh);
            api.defaults.headers.common["Authorization"] =
              "Bearer " + localStorage.getItem("access");
            return api(originalRequest);
          }
        });
    }
    return Promise.reject(error);
  }
);

export default api;
