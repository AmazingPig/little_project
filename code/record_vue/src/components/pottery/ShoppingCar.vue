<template>
    <div>
      <el-row :gutter="20">
        <el-col :span="12" :offset="6">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span style="font-size: 35px;">{{username}}的购物车</span>
            </div>

            <hr>
            <div v-for="course in courses">
              <!--课程信息部分-->
              <el-col :span="18">
                <div style="display: inline-block; position:relative; height:200px;width:600px;">
                  <div class="title">{{course.title}}</div>
                  <div class="brief">{{course.brief}}</div>
                  <div class="footer">
                    <span>价格：{{course.price}}元</span>
                    <span @click="showOrderInfo('course', course)" style="margin-left: 100px; color: #3a8ee6; cursor: pointer"><i class="el-icon-shopping-cart-2" style="margin-right: 5px;"></i>购买</span>
                    <span @click="showDrop('course', course.id)" style="margin-left: 20px; color: #3a8ee6; cursor: pointer">移出购物车</span>
                  </div>

                </div>
              </el-col>
              <!--课程  图片部分-->
              <el-col :span="6">
                <img :src="get_img_path(course.img)" width="200px" height="200px">
              </el-col>

              <hr>
            </div>


            <div v-for="good in goods">
              <!--商品信息部分-->
              <el-col :span="18">
                <div style="display: inline-block; position:relative; height:200px;width:600px;">
                  <div class="title">{{good.title}}</div>
                  <div class="brief">{{good.brief}}</div>
                  <div class="footer">
                    <span>价格：{{good.price}}元</span>
                    <span @click="showOrderInfo('good', good)" style="margin-left: 100px; color: #3a8ee6; cursor: pointer"><i class="el-icon-shopping-cart-2" style="margin-right: 5px;"></i>购买</span>
                    <span @click="showDrop('good', good.id)" style="margin-left: 20px; color: #3a8ee6; cursor: pointer">移出购物车</span>
                  </div>
                </div>
              </el-col>
              <!--商品图片部分-->
              <el-col :span="6">
                <img :src="get_img_path(good.img)" width="200px" height="200px">
              </el-col>

              <hr>

            </div>
          </el-card>
        </el-col>
      </el-row>

      <!--确认订单信息框-->
      <el-dialog title="确认订单信息" :visible.sync="isShow" width="30%" :before-close="handleClose">
        <div style="font-size: 16px;">
          <div>类型：<span v-if="is_course">课程</span><span v-else>商品</span></div>
          <div>名称：{{this.form.title}}</div>
          <div>价格：{{this.form.price}}</div>
          <div>
            选择优惠券：
            <el-select v-model="form.coupon" placeholder="请选择优惠券">
              <el-option v-for="coupon in coupons" :key="coupon" :label="coupon.title" :value="coupon.id"></el-option>
            </el-select>
          </div>
          <div>
            付款方式：
            <el-select v-model="form.payment" placeholder="请选择付款方式">
              <el-option label="支付宝" value="1">支付宝</el-option>
              <el-option label="微信" value="2">微信</el-option>
            </el-select>
          </div>
        </div>

        <span slot="footer" class="dialog-footer">
          <el-button @click="isShow = false">取 消</el-button>
          <el-button type="primary" @click="pay()">确 定</el-button>
        </span>
      </el-dialog>

      <!--确认是否移出购物车框-->
      <el-dialog title="提示" :visible.sync="isDrop" width="30%" :before-close="handleClose">
        <span>是否确认移出购物车？</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="isDrop = false">取 消</el-button>
          <el-button type="primary" @click="drop()">确 定</el-button>
        </span>
      </el-dialog>

    </div>
</template>

<script>
    export default {
        name: "shopping-car",
        data(){
          return {
            username: this.$store.state.user,
            courses: [],
            goods: [],
            coupons: [],
            isShow: false,
            isDrop: false,
            type: '',
            choice_id: '',
            form: {
              type: '',
              choice_id: '',
              title: '',
              price: '',
              coupon: '',
              payment: '', // 付款方式
            },
          }
        },
        computed:{
          is_course(){
            if(this.form.type=='course'){
              return true;
            }else{
              return false;
            }
          }
        },
        methods:{
          // 获取购物车信息
          get_shopping_car_info(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/shopping_car/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'get'
            }).then(function(data){
              if(data.data.status==200){
                that.courses = data.data.courses;
                that.goods = data.data.goods;
              }
            })
          },
          // 获取用户拥有的优惠券
          get_coupons(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/coupons/?id=${that.$store.state.user_id}&username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'get'
            }).then(function(data){
              if(data.data.status==200){
                that.coupons = data.data.coupons;
              }
            })
          },
          // 拼接图片路径
          get_img_path(path){
            return `http://${this.$store.state.host}:8000/${path}`
          },
          // 显示确认订单框
          showOrderInfo(type, item){
            this.isShow = true;
            this.form.type = type;
            this.form.choice_id = item.id;
            this.form.price = item.price;
            this.form.title = item.title;
          },
          // 前往付款
          pay(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/pay/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'post',
              data: {type: that.form.type, choice_id: that.form.choice_id, price: that.form.price, coupon: that.form.coupon, payment: that.form.payment}
            }).then(function(data){
              location.href = data.data.pay_url;
            })
          },
          // 显示确认是否删除框
          showDrop(type, id){
            this.isDrop = true;
            this.type = type;
            this.choice_id = id;
          },
          // 移除购物车
          drop(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/shopping_car/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'delete',
              data: {type: that.type, id: that.choice_id}
            }).then(function(data){
              that.isDrop = false;
              that.get_shopping_car_info();
              if(data.data.status==200){
                that.$message({
                  message: data.data.data,
                  type: 'success',
                  offset: 60,
                  center: true,
                  showClose: true
                })
              }else{
                that.$message.error({
                  message: data.data.data,
                  offset: 60,
                  center: true,
                  showClose: true
                })
              }
            })
          }
        },
        mounted(){
          this.get_shopping_car_info();
          this.get_coupons();
        }
    }
</script>

<style scoped>
  .el-row {
    margin-bottom: 20px;
  }
  .el-row:last-child {
      margin-bottom: 0;
    }
  .el-col {
    border-radius: 4px;
  }
.big-title{
  font-size: 35px;
  color: #333333;
  margin-top: 30px;
}
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 100%;
    margin-top: 50px;
  }
  .title{
    margin-top: 20px;
    font-weight: bolder;
    font-size: 25px;
  }
  .brief{
    margin-top:20px;
    font-size: 20px;
  }
  .footer{
    position: absolute;
    bottom: 20px;
  }
</style>
