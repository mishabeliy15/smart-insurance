import CompanyService from "./../services/company.services";
import { CLEAR_MESSAGE, SET_MESSAGE } from "./types";

export const createCompany = (data) => (dispatch) =>
  CompanyService.createCompany(data)
    .then(() => {
      dispatch({ type: CLEAR_MESSAGE });
      return Promise.resolve();
    })
    .catch((error) => {
      dispatch({ type: SET_MESSAGE, payload: error.response.data });
      return Promise.reject();
    });
