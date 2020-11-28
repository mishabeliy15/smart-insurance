import axios from "axios";
// import history from "./history";

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

// services.interceptors.response.use(
//   (response) => {
//     return response;
//   },
//   function (error) {
//     const originalRequest = error.config;
//
//     if (
//       error.response.status === 401 &&
//       originalRequest.url === `${API_URL}auth/jwt/refresh/`
//     ) {
//       history.push("/login");
//       return Promise.reject(error);
//     }
//
//     if (error.response.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true;
//       const refreshToken = localStorage.getItem("refresh");
//       return services
//         .post("auth/jwt/refresh/", {
//           refresh: refreshToken,
//         })
//         .then((res) => {
//           if (res.status in [200, 201]) {
//             localStorage.setToken("access", res.data.access);
//             localStorage.setToken("refresh", res.data.refresh);
//             services.defaults.headers.common["Authorization"] =
//               "Bearer " + localStorage.getItem("access");
//             return services(originalRequest);
//           }
//         });
//     }
//     return Promise.reject(error);
//   }
// );

export default api;
