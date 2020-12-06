import axios from "../helpers/axios";

class ContractService {
  BASE_API_URL = "contracts/";
  MY_API_URL = `${this.BASE_API_URL}my/`;

  createContract(companyId, month) {
    return axios
      .post(this.BASE_API_URL, {
        months: month,
        company: companyId,
      })
      .then((response) => response.data);
  }

  getMyContracts = () =>
    axios.get(this.MY_API_URL).then((response) => response.data.results);

  deleteContract = (id) =>
    axios
      .delete(`${this.BASE_API_URL}${id}/`)
      .then((response) => response.data);
}

export default new ContractService();
