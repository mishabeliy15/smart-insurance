import axios from "../helpers/axios";

class CompanyService {
  BASE_API_URL = "companies/";
  MY_COMPANY_API_URL = `${this.BASE_API_URL}my/`;

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

  myCompanies() {
    return axios(this.MY_COMPANY_API_URL).then(
      (response) => response.data.results
    );
  }
}

export default new CompanyService();
