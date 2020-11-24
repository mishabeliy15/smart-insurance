import { combineReducers } from "redux";
import auth from "./auth";
import { routerReducer } from "react-router-redux";
import message from "./message";

export default combineReducers({
  routing: routerReducer,
  auth,
  message,
});
