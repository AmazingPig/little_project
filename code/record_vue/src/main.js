// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import axios from 'axios';
import 'element-ui/lib/theme-chalk/index.css';
import store from './store'
import Share from 'vue-social-share'
import 'vue-social-share/dist/client.css'


Vue.prototype.$axios = axios;
Vue.use(ElementUI);
Vue.use(Share);

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
});

router.beforeEach((to,from,next)=>{
  if(to.path!="/"){
    // 如果去往的不是首页，则判断是否登陆
    if(store.state.user == ""){
      next('/');
      store.commit("please_login", true);
    }else{
      next()
    }
  }else{
    next();
  }
});
