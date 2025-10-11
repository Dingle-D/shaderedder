import ApiService from "@/common/api.service";
import JwtService from "@/common/jwt.service";


const state = {
  errors: null,
  user: {},
  isAuthenticated: !!JwtService.getToken()
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  }
};

const mutations = {
  SET_ERROR(state, error) {
    state.errors = error;
  },
  SET_AUTH(state, token_data) {
    state.isAuthenticated = true;
    state.errors = null;
    JwtService.saveToken(token_data.type, token_data.token);
  },
  SET_USER_INFO(state, user) {
    state.isAuthenticated = true;
    state.user = user;
    state.errors = null;
  },
  PURGE_AUTH(state) {
    state.isAuthenticated = false;
    state.user = {}
    state.errors = null;
    JwtService.destroyToken();
  }
};

const actions = {
async LOGIN(context, credentials) {
    try {
      const params = new URLSearchParams();
      params.append('grant_type', 'password');
      params.append('username', credentials.username);
      params.append('password', credentials.password);
      params.append('captcha', credentials.captcha);

      const { data } = await ApiService.post("login", params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'
        }
      });

      context.commit('SET_AUTH', {
        type: data.token_type,
        token: data.access_token
      });

      return data;
    } catch (error) {
      context.commit('SET_ERROR', error.response?.data.detail);
      
      throw error.response?.data.detail;
    }
  },

  // does not make query to backend. just adds given params into storage.
  LOGIN_FORCE(context, token) {
    try {
      const tmptoken = {
        type: token.token_type,
        token: token.access_token
      };
      context.commit('SET_AUTH', {
        type: token.token_type,
        token: token.access_token
      });
    } catch (error) {
      context.commit('SET_ERROR', error.response?.data.detail);
      throw error.response?.data.detail;
    }
  },

  LOGOUT(context) {
    context.commit('PURGE_AUTH');
  },

  async REGISTER(context, credentials) {
    try {
      const { data } = await ApiService.post("register", credentials);
      return data;
    } catch (error) {
      context.commit('SET_ERROR', error.response?.data.detail);
      throw error;
    }
  },

  async CONFIRM(context, token) {
    try {
      const { data } = await ApiService.post(`register/confirm?token=${token}`);
      return data;
    }
    catch (error) {
      context.commit('SET_ERROR', error.response?.data.detail);
      throw error;
    }
  },

  async CHECK_AUTH(context) {
    if (JwtService.getToken()) {
      ApiService.setJwtHeader();
      try {
        const user = await ApiService.post("login/test-token");
        context.commit('SET_USER_INFO', user.data);
      } catch (error) {
        console.error("Token is invalid. Purging authentication.");
        context.commit('PURGE_AUTH');
      }
    } else {
      context.commit('PURGE_AUTH');
    }
  }
};

export default {
  state,
  actions,
  mutations,
  getters
}
