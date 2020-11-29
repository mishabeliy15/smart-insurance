import { END_LOADING, IS_LOADING, REFRESH_SENSORS, SET_MESSAGE } from "./types";
import SensorService from "../services/sensor.service";

export const getMySensors = () => (dispatch) => {
  dispatch({ type: IS_LOADING });
  SensorService.mySensors().then((sensors) =>
    dispatch({ type: REFRESH_SENSORS, payload: sensors })
  );
};

export const addSensor = (uuid, sensorType) => (dispatch) => {
  dispatch({ type: IS_LOADING });
  SensorService.addSensor(uuid, sensorType)
    .then((data) => {
      dispatch({ type: REFRESH_SENSORS, payload: data });
      return Promise.resolve();
    })
    .catch((error) => {
      dispatch({ type: END_LOADING });
      dispatch({ type: SET_MESSAGE, payload: error.response.data });
      return Promise.reject();
    });
};
