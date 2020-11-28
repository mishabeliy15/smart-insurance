import AuthService from "../services/auth.service";
import {
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  LOGOUT,
  REGISTER_FAIL,
  REGISTER_SUCCESS,
  SET_MESSAGE,
} from "./types";

export const login = (username, password) => (dispatch) => {
  return AuthService.login(username, password)
    .then((data) => {
      dispatch({
        type: LOGIN_SUCCESS,
        payload: { user: data },
      });

      return Promise.resolve();
    })
    .catch((error) => {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.reason ||
        error.toString();

      dispatch({
        type: LOGIN_FAIL,
      });

      dispatch({
        type: SET_MESSAGE,
        payload: message,
      });

      return Promise.reject();
    });
};

export const register = ({ userData }) => (dispatch) => {
  return AuthService.register(userData).then(
    (response) => {
      dispatch({
        type: REGISTER_SUCCESS,
      });

      dispatch({
        type: SET_MESSAGE,
      });

      return Promise.resolve();
    },
    (error) => {
      const message =
        (error.response && error.response.data && error.response.data.detail) ||
        error.message ||
        error.toString();

      dispatch({
        type: REGISTER_FAIL,
      });

      dispatch({
        type: SET_MESSAGE,
        payload: message,
      });

      return Promise.reject();
    }
  );
};

export const logout = () => (dispatch) => {
  AuthService.logout();

  dispatch({
    type: LOGOUT,
  });
};
