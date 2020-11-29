import { END_LOADING, IS_LOADING, REFRESH_SENSORS } from "../actions/types";

const initialState = { isLoading: true, sensors: [] };

function sensorReducer(state = initialState, action) {
  const { type, payload } = action;

  switch (type) {
    case IS_LOADING:
      return { isLoading: true, ...state };
    case REFRESH_SENSORS:
      return { isLoading: false, sensors: payload };
    case END_LOADING:
      return { isLoading: false, ...state };
    default:
      return state;
  }
}

export default sensorReducer;
