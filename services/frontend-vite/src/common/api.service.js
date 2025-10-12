import axios from "axios";
import JwtService from "@/common/jwt.service";

//const api_url = process.env.VUE_APP_API_URL;
//const api_url = "http://localhost:5000/api/v1";
const api_url = import.meta.env.VITE_API_URL;

const ApiService = {
  getApiUrl() {
    return api_url;
  },

  init() {
    axios.defaults.baseURL = api_url;
    axios.defaults.withCredeintials = true;
  },

  setJwtHeader() {
    axios.defaults.headers.common[
      "Authorization"
    ] = `${JwtService.getToken()}`;
  },

  removeJwtHeader() {
    delete axios.defaults.headers.common['Authorization'];
  },

  query(resource, params) {
    return axios.get(resource, params).catch(error => {
      throw new Error(`[Shaderedder] ApiService ${error}`);
    });
  },

  get(resource, slug = "") {
    return axios.get(`${resource}/${slug}`).catch(error => {
      throw new Error(`[Shaderedder] ApiService ${error}`);
    });
  },

  post(resource, params, config = {}) {
    return axios.post(`${resource}`, params, config);
  },

  update(resource, slug, params) {
    return axios.put(`${resource}/${slug}`, params);
  },

  put(resource, params) {
    return axios.put(`${resource}`, params);
  },

  delete(resource) {
    return axios.delete(resource).catch(error => {
      throw new Error(`[Shaderedder] ApiService ${error}`);
    });
  }
};

export default ApiService;


