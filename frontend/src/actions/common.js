import { CHANGE_LANGUAGE } from "./types";
import i18n from "../i18n";

export const changeLanguage = (lang) => (dispatch) => {
  localStorage.setItem("i18nextLng", lang);
  i18n.changeLanguage(lang);

  dispatch({
    type: CHANGE_LANGUAGE,
    payload: lang,
  });
};
