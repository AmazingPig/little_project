import Vue from 'vue'
import Vuex from 'vuex'
import router from './router'

Vue.use(Vuex);

export default new Vuex.Store({
  state:{
    host: "60.205.227.178",
    user: "",
    user_id: null,
    token: "",
    please_login: false,
    loginVisible: false,
    regVisible: false,
  },
  getters:{
    user(state){
      return state.user;
    },
    token(state){
      return state.token;
    },
    please_login(state){
      return state.please_login;
    },
    loginVisible(state){
      return state.loginVisible;
    },
    regVisible(state){
      return state.regVisible;
    },
  },
  mutations:{
    // 登陆后将用户名、id和token放入store
    change_user(state, data){
      state.user = data;
    },
    change_user_id(state, data){
      state.user_id = data;
    },
    change_token(state, data){
      state.token = data;
    },
    // 注销时清空用户名和token
    logout(state){
      state.user = "";
      state.token = "";
    },
    // 控制"请先登陆"框的显示或隐藏
    please_login(state, status){
      state.please_login = status;
    },
    // 控制"登陆框"的显示或隐藏
    change_loginVisible(state, status){
      state.loginVisible = status
    },
    // 控制"注册框"的显示或隐藏
    change_regVisible(state, status){
      state.regVisible = status;
    },
  }
})


