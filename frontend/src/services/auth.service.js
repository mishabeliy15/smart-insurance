import axios from "../helpers/axios";

class AuthService {
  REGISTER_API_URL = "/auth/users/";
  LOGIN_API_URL = "/auth/jwt/create/";
  MY_API_URL = "/auth/users/me/";

  login(username, password) {
    return axios
      .post(this.LOGIN_API_URL, { username, password })
      .then((response) => {
        localStorage.setItem("access", response.data.access);
        localStorage.setItem("refresh", response.data.refresh);
        return this.my().then((user) => {
          localStorage.setItem("user", JSON.stringify(user));
          return user;
        });
      });
  }

  my() {
    return axios.get(this.MY_API_URL).then((response) => response.data);
  }

  register(userData) {
    return axios.post(this.REGISTER_API_URL, userData).then((response) => {
      return response.data;
    });
  }

  logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  }
}

export default new AuthService();
