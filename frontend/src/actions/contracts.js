import { LOADING_CONTRACTS, REFRESH_CONTRACTS } from "./types";
import ContractService from "../services/contract.services";
import { getPersonalCompanyPrices } from "./company";

export const getContracts = () => (dispatch) => {
  dispatch({ type: LOADING_CONTRACTS });
  return ContractService.getMyContracts().then((data) => {
    dispatch({ type: REFRESH_CONTRACTS, payload: data });
    return Promise.resolve();
  });
};

export const getContractsWithCompanies = () => (dispatch) =>
  dispatch(getPersonalCompanyPrices()).then(() => dispatch(getContracts()));

export const deleteContract = (id) => (dispatch) =>
  ContractService.deleteContract(id).then(() => dispatch(getContracts()));
