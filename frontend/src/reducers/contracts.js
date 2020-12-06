import {
  CONTRACTS_LOADED,
  LOADING_CONTRACTS,
  REFRESH_CONTRACTS,
} from "../actions/types";

const initialState = { isLoading: true, contracts: [] };

function contractsReducer(state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case LOADING_CONTRACTS:
      return { isLoading: true, ...state };
    case REFRESH_CONTRACTS:
      return { isLoading: false, contracts: payload };
    case CONTRACTS_LOADED:
      return { isLoading: false, ...state };
    default:
      return state;
  }
}

export default contractsReducer;
