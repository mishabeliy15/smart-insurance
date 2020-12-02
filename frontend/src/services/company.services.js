import axios from "../helpers/axios";

class CompanyService {
  BASE_API_URL = "companies/";

  createCompany(inputData) {
    let data = new FormData();
    for (let key in inputData) {
      data.append(key, inputData[key]);
    }
    let config = {
      method: "post",
      url: this.BASE_API_URL,
      headers: data.getHeaders,
      data: data,
    };
    return axios(config).then((response) => response.data);
  }
}

export default new CompanyService();
