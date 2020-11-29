import axios from "../helpers/axios";

class SensorService {
  BASE_SENSOR_API = "/sensors/";
  GET_MY_SENSORS_API_URL = `${this.BASE_SENSOR_API}my`;
  ADD_SENSOR_API_URL = this.BASE_SENSOR_API;

  mySensors() {
    return axios
      .get(this.GET_MY_SENSORS_API_URL)
      .then((response) => response.data.results);
  }

  addSensor(uuid, sensorType) {
    return axios
      .post(this.ADD_SENSOR_API_URL, { uuid: uuid, sensor_type: sensorType })
      .then((response) => response.data);
  }
}

export default new SensorService();
