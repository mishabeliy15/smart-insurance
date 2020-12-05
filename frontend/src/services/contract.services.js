import axios from "../helpers/axios";

class ContractServices {
  BASE_API_URL = "contracts/";

  createContract(companyId, month) {
    return axios
      .post(this.BASE_API_URL, {
        months: month,
        company: companyId,
      })
      .then((response) => response.data);
  }
}

export default new ContractServices();
