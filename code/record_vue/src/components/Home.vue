<template>
  <div>
    <div v-if="user">
      <div class="welcome">欢迎登陆</div>
    </div>
    <div v-else>
      <div class="welcome">欢迎使用</div>
      <div class="log_reg">
        <span @click="change_loginVisible(true)" class="login">登陆</span>
        |
        <span @click="change_regVisible(true)" class="register">注册</span>
      </div>
    </div>

    <div class="desc">本网站只用于个人学习实践，没有任何真实性，素材源于网络。</div>
    <div class="desc">付款购买功能没有完成，请勿付款，无实物出售</div>
    <div class="desc">朗读文章功能在线上环境暂时无法使用，原因未知</div>

    <el-dialog title="登陆" :visible.sync="loginVisible" width="25%" center="true">
      <el-form label-width="80px" style="margin-top: 10px;">
        <el-form-item label="用户名" style="margin-left: -10px;">
          <el-input v-model="username" @focus="clearError"></el-input>
        </el-form-item>
        <el-form-item label="密码" style="margin-left: -10px;">
          <el-input type="password" v-model="password" @focus="clearError" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="change_loginVisible(false)">取 消</el-button>
        <el-button type="primary" @click="login">确 定</el-button>
        <span class="error_info" ref="error_info"></span>
      </div>
    </el-dialog>

    <el-dialog title="注册" :visible.sync="regVisible" width="25%" center="true">
      <el-form label-width="80px" style="margin-top: 10px;">
        <el-form-item label="用户名" style="margin-left: -10px;">
          <el-input v-model="username" @focus="clearError"></el-input>
        </el-form-item>
        <el-form-item label="密码" style="margin-left: -10px;">
          <el-input type="password" v-model="password" @focus="clearError" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="change_regVisible(false)">取 消</el-button>
        <el-button type="primary" @click="register">确 定</el-button>
        <span class="error_info" ref="reg_error_info"></span>
      </div>
    </el-dialog>

  </div>
</template>

<script>
    export default {
        name: "home",
        data(){
          return {
            formLabelWidth: 60,
            username: "",
            password: "",
          }
        },
        computed:{
          user(){
            return this.$store.getters.user;
          },
          loginVisible(){
            return this.$store.getters.loginVisible;
          },
          regVisible(){
            return this.$store.getters.regVisible;
          }
        },
        methods:{
          // 登陆
          login(){
            let that = this;
            this.$axios.request({
              url: "http://" + that.$store.state.host + ":8000/login/",
              method: "post",
              data: {username: that.username, password: that.password},
            }).then(function(data){
              if(data.data.status==200){
                console.log(data.data.data)
                console.log(data.data)
                that.$store.commit("change_user", that.username);
                that.$store.commit("change_user_id", data.data.data.user_id);
                that.$store.commit("change_token", data.data.data.token);
                that.$store.commit("change_loginVisible", false);
                that.$message({
                  message: "登陆成功",
                  type: "success",
                  center: true,
                  offset: 60,
                  showClose: true,
                })
              }else{
                that.$refs.error_info.innerText = data.data.data;
              }
            })
          },
          // 当input获取焦点时清楚错误信息
          clearError(){
            this.$refs.error_info.innerText = "";
            this.$refs.reg_error_info.innerText = "";
          },
          // 关闭或打开登陆框
          change_loginVisible(status){
            this.$store.commit("change_loginVisible", status);
            this.username = "";
            this.password = "";
          },
          // 关闭或打开注册框
          change_regVisible(status){
            this.$store.commit("change_regVisible", status);
            this.username = "";
            this.password = "";
          },
          // 注册
          register(){
            if(this.username==""){
              this.$refs.reg_error_info.innerText = "请输入用户名！";
            }else if(this.password.length < 4){
              this.$refs.reg_error_info.innerText = "密码不能少于4位！";
            }else{
              let that = this;
              this.$axios.request({
                url: "http://" + that.$store.state.host + ":8000/register/",
                method: "post",
                data: {username: that.username, password: that.password},
              }).then(function(data){
                if(data.data.status==200){
                  that.$store.commit("change_user", that.username);
                  that.$store.commit("change_token", data.data.data);
                  that.$store.commit("change_regVisible", false);
                  that.$message({
                    message: "注册成功",
                    type: "success",
                    center: true,
                    offset: 60,
                    showClose: true,
                  })
                }else{
                  that.$refs.reg_error_info.innerText = data.data.data;
                }
              })
            }
          }
        },
    }
</script>

<style scoped>
 .welcome{
   color: rgb(102, 177, 255);
   font-size: 80px;
   margin-top: 250px;
   margin-left: 780px;
 }
 .desc{
   color: red;
   font-size: 35px;
   margin-top: 50px;
   text-align: center;
 }
  .log_reg{
    color: rgb(102, 177, 255);
    font-size: 30px;
    margin-top: 80px;
    margin-left: 870px;
  }
  .login, .register{
    cursor: pointer;
  }
  .login:hover, .register:hover{
    color: #076ce6;
  }
  .error_info{
    color: red;
    font-size: 14px;
  }
  .dialog-footer{
    margin-top: -10px;
  }
</style>
