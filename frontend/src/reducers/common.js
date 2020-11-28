import { CHANGE_LANGUAGE } from "../actions/types";

const lang = localStorage.getItem("i18nextLng");

const initialState = {
  lang: lang || "en",
};

function commonReducer(state = initialState, action) {
  const { type, payload } = action;
  switch (type) {
    case CHANGE_LANGUAGE:
      return {
        ...state,
        lang: payload,
      };
    default:
      return state;
  }
}

export default commonReducer;
