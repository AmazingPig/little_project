<template>
  <div id="app">
    <el-menu :default-active="activeIndex" class="el-menu-demo" router=true mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="/blog">博客功能</el-menu-item>
      <el-menu-item index="/code/record">代码记录</el-menu-item>
      <el-menu-item index="/school_system/classes">教务系统</el-menu-item>
      <el-menu-item index="/pottery">春泥造物</el-menu-item>
      <el-submenu index="2">
        <template slot="title">其他功能</template>
      </el-submenu>

      <div v-if="user" class="dropdownMenu">
        <span v-text="$store.state.user" class="username"></span>
        <el-dropdown trigger="hover">
          <span class="el-dropdown-link">
            个人中心<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <span><el-dropdown-item><i class="el-icon-user"></i>个人信息</el-dropdown-item></span>
            <span @click="to_shopping_car"><el-dropdown-item><i class="el-icon-shopping-cart-2"></i>购物车</el-dropdown-item></span>
            <span @click="logout"><el-dropdown-item divided>注销</el-dropdown-item></span>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <div v-else></div>

    </el-menu>


    <!--提示登陆-->
    <el-dialog title="提示" :visible="please_login" width="30%" :before-close="handleClose"><span>请先登陆！</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel_please_login">取 消</el-button>
        <el-button type="primary" @click="confirm_please_login">确 定</el-button>
      </span>
    </el-dialog>

    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App',
  data(){
    return {
      activeIndex: "/"
    }
  },
  computed:{
    user(){
      return this.$store.getters.user;
    },
    please_login(){
      return this.$store.getters.please_login;
    }
  },
  methods:{
    // 点击触发注销
    logout(){
      let that = this;
      this.$axios.request({
        url: "http://" + that.$store.state.host + ":8000/logout/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
        method: "get",
      }).then(function(data){
        if(data.data.status==200){
          that.$store.commit("logout");
          window.location.href = "/";
          that.$message({
            message: "注销成功",
            type: "success",
            center: true,
          })
        }else{
          alert(data.data.data)
        }
      })
    },
    // 点击取消请先登陆的提示框
    cancel_please_login(){
      this.$store.commit("please_login", false);
    },
    // 点击确定请先登陆的提示框，并跳出登陆框
    confirm_please_login(){
      this.$store.commit("please_login", false);
      this.$store.commit("change_loginVisible", true)
    },
    // 跳转到购物车界面
    to_shopping_car(){
      this.$router.push({name: 'shopping_car'})
    }
  },
  beforeCreate(){
    // 第一次访问时不走路由守卫，在这里检查是否登陆
    if(this.$route.path != "/"){
     if(this.$store.state.user == ""){
       this.$router.push({"path": "/"});
       this.$store.commit("please_login", true);
     }
    }
  }
}
</script>

<style>
.el-menu{
  display: flex;
  align-items: center;
  justify-content: center;
}
  .dropdownMenu{
    position: absolute;
    right: 25px;
    top: 17px;
  }
    .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .username{
    color: #409EFF;
    margin-right: 10px;
    font-size: 17px;
    cursor: pointer;
  }

</style>
