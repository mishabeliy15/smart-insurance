import CompanyService from "./../services/company.services";
import {
  CLEAR_MESSAGE,
  LOADING_COMPANIES,
  REFRESH_COMPANIES,
  SET_MESSAGE,
} from "./types";

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

export const getMyCompany = () => (dispatch) => {
  dispatch({ type: LOADING_COMPANIES });
  return CompanyService.myCompanies().then((data) => {
    dispatch({ type: REFRESH_COMPANIES, payload: data });
    return Promise.resolve();
  });
};

export const deleteCompany = (id) => (dispatch) =>
  CompanyService.deleteCompany(id).then(() => dispatch(getMyCompany()));

export const getCompany = (id) => (dispatch) => CompanyService.getCompany(id);

export const editCompany = (id, data) => (dispatch) =>
  CompanyService.editCompany(id, data)
    .then(() => {
      dispatch({ type: CLEAR_MESSAGE });
      return Promise.resolve();
    })
    .catch((error) => {
      dispatch({ type: SET_MESSAGE, payload: error.response.data });
      return Promise.reject();
    });
