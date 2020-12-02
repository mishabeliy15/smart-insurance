import {
  COMPANIES_LOADED,
  LOADING_COMPANIES,
  REFRESH_COMPANIES,
} from "../actions/types";

const initialState = { isLoading: true, companies: [] };

function companyReducer(state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case LOADING_COMPANIES:
      return { isLoading: true, ...state };
    case REFRESH_COMPANIES:
      return { isLoading: false, companies: payload };
    case COMPANIES_LOADED:
      return { isLoading: false, ...state };
    default:
      return state;
  }
}

export default companyReducer;
