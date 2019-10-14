<template>
    <div>
      <div class="shopping_car" @click="to_shopping_car()"><i class="el-icon-shopping-cart-2" style="margin-right: 5px;"></i>我的购物车</div>
      <div class="coupon" @click="coupon_div = true">领取新用户优惠券</div>
      <el-dialog title="提示" :visible.sync="coupon_div" width="30%" :before-close="handleClose">
        <el-form ref="form" :model="form" label-width="200px">
          <el-form-item label="选择优惠券">
            <el-select v-model="form.coupon" placeholder="请选优惠券">
              <div v-for="coupon in coupons">
                <el-option :label="coupon.title" :value="coupon.id"></el-option>
              </div>
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="coupon_div = false">取 消</el-button>
          <el-button type="primary" @click="add_coupon()">确 定</el-button>
        </span>
      </el-dialog>

      <div class="center" style="color:orangered; margin-top:50px;">
        <h1 style="font-weight: bolder;">春泥造物陶艺体验工坊</h1>
        <div style="margin-left: 300px;">----让情怀落地，化春泥护花</div>
      </div>

      <!--poll-->
      <div class="round-img">
        <el-carousel :interval="4000" type="card" height="300px">
          <el-carousel-item v-for="item in imgs" :key="item">
            <h3 class="medium"><img :src="item" height="300px" width="662px"></h3>
          </el-carousel-item>
        </el-carousel>
      </div>

      <div class="yellow"></div>

      <!--项目介绍-->
      <div class="center" style="background-color: #f9f9f9;padding-bottom:30px;">
        <div class="title-background"><h3 class="title">项目介绍</h3></div>
        <div style="margin-top: 50px;">
          <el-row :gutter="20">
            <el-col :span="6" :offset="6">
              <div class="grid-content bg-purple company-intro">
                <div><span class="font-bolder">我们</span>：山东大学春泥造物创业团队</div>
                <div style="margin-top: 50px;"><span class="font-bolder">业务</span>：致力于打造以传统文化体验为核心的结合了陶艺、茶艺、花艺、水拓画、流体画等多种体验项目的生活美学空间，努力成为校园文创与陶艺订制的行业标杆。</div>

              </div>
            </el-col>

            <el-col :span="6" :offset="1">
              <div class="grid-content bg-purple company-intro">
                <div><span class="font-bolder">定位</span>：为人们提供工艺美术体验与传统文化交流与认知的传统文化体验式创业项目</div>
                <div><span class="font-bolder">使命</span>：成为山东地区以传统文化为依托的文化服务产业标杆</div>
                <div><span class="font-bolder">愿景</span>：非凡匠心，千年工艺展露新颜。知行合一，传统文化薪火相传。</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <div class="yellow"></div>

      <!--教室介绍-->
      <div class="center">
        <div class="title-background"><h3 class="title">教室展示</h3></div>
        <div style="text-align: center;margin-bottom: 20px; margin-top:10px;">少儿陶艺教育中心(300余平方米) 研发了提升儿童创新能力的陶艺教程</div>
        <el-row :gutter="20">
          <el-col :span="12" :offset="6">
            <div v-for="img in room_imgs">
              <img :src="img">
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="yellow"></div>

      <!--商品展示-->
      <div>
        <div class="title-background" style="margin-left: 770px;"><h3 class="title">商品展示</h3></div>
        <div style="margin-top: 50px;">
          <el-row :gutter="20">
            <el-col :span="16" :offset="4">
              <div class="company-intro" v-for="item in goods">
                <el-card :body-style="{ padding: '0px' }" style="margin-left: 40px">
                  <img :src="get_img_path(item)" class="image" height="360px" width="360px;">
                  <div style="padding: 14px;">
                    <span>{{item.title}}</span><span style="float: right;font-weight: lighter;">{{item.price}}元</span>
                    <div class="bottom clearfix">
                      <span class="brief">{{item.brief}}</span>
                      <el-button type="text" class="button" style="margin-left:10px; font-size: 15px;">购买</el-button>
                      <el-button type="text" class="button" style="font-size: 15px;" @click="add_shopping_car('good', item.id)">+ 购物车</el-button>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <div class="yellow"></div>

      <!--课程展示-->
      <div>
        <div class="title-background" style="margin-left: 770px;"><h3 class="title">课程展示</h3></div>
        <div style="margin-top: 50px;">
          <el-row :gutter="20">
            <el-col :span="16" :offset="4">
              <div class="company-intro" v-for="(item, index) in courses">
                <el-card :body-style="{ padding: '0px' }" style="margin-left: 40px">
                  <img :src="get_img_path(item)" class="image" height="360px" width="360px;">
                  <div style="padding: 14px;">
                    <span>{{item.title}}</span>
                    <span class="type">（{{item.type}}）</span>
                    <span style="float: right;font-weight: lighter;">{{item.price}}元</span>
                    <div class="bottom clearfix">
                      <span class="brief">{{item.brief}}</span>
                      <span><el-button type="text" class="button" style="margin-left:10px; font-size: 15px;">购买</el-button></span>
                      <el-button type="text" class="button" style="font-size: 15px;" @click="add_shopping_car('course', item.id)">+ 购物车</el-button>
                    </div>
                  </div>
                </el-card>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>

      <div class="yellow"></div>

      <!--老师介绍-->
      <div class="center">
        <div class="title-background"><h3 class="title">老师介绍</h3></div>
        <div style="margin-top: 50px;">
          <el-row :gutter="20">
            <el-col :span="12" :offset="6">
              <div v-for="teacher in teacher_imgs">
                <img :src="teacher" style="margin-top:-5px;">
              </div>
            </el-col>
          </el-row>
        </div>
      </div>


      <!--页底-->
      <div class="footer">
        <div>关于我们 | 春泥造物陶艺体验工坊</div>
        <div>地址：山东省济南市xxxxxxx</div>
        <div><span>电话：8888888888</span><span>邮箱：8888888@163.com</span></div>
      </div>
    </div>
</template>

<script>
    export default {
        name: "index",
        data(){
          return {
            coupon_div: false,
            imgs: ["static/pottery/poll/春泥3.png", "static/pottery/poll/春泥2.jpg", "static/pottery/poll/春泥1.png"],
            room_imgs: ["static/pottery/classroom/1.jpg", "static/pottery/classroom/2.jpg"],
            teacher_imgs: ["static/pottery/teacher/1.jpg", "static/pottery/teacher/2.jpg", "static/pottery/teacher/3.jpg", "static/pottery/teacher/4.jpg", "static/pottery/teacher/5.jpg"],
            goods: [],
            courses: [],
            coupons: [],
            form: {
              coupon: '',
            }
          }
        },
        methods:{
          // 拼接商品图片路径
          get_img_path(item){
            return `http://${this.$store.state.host}:8000/${item.img}`
          },
          // 获取商品信息
          get_goods(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/goods/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'get'
            }).then(function(data){
              if(data.data.status==200){
                that.goods = data.data.goods;
              }
            })
          },
          // 获取课程信息
          get_courses(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/courses/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'get'
            }).then(function(data){
              if(data.data.status==200){
                that.courses = data.data.courses;
              }
            })
          },
          // 获取优惠券信息
          get_coupons(){
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/coupons/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'get'
            }).then(function(data){
              if(data.data.status==200){
                that.coupons = data.data.coupons;
              }
            })
          },
          // 领取优惠券
          add_coupon(){
            let id = this.form.coupon;
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/coupons/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'post',
              data: {id: id}
            }).then(function(data){
              if(data.data.status==200){
                that.coupon_div = false;
                that.form.coupon = '';
                that.$message({
                  type: 'success',
                  message: data.data.data,
                  offset: 60,
                  showClose: true,
                  center: true,
                })
              }else if(data.data.status==450){
                that.$message.error({
                  message: data.data.data,
                  offset: 60,
                  showClose: true,
                  center:true,
                })
              }
            })
          },
          // 添加进购物车
          add_shopping_car(type, id){  // 传入course/good，id
            let that = this;
            this.$axios.request({
              url: `http://${that.$store.state.host}:8000/api/pottery/shopping_car/?username=${that.$store.state.user}&token=${that.$store.state.token}`,
              method: 'post',
              data: {type: type, id: id}
            }).then(function(data){
              if(data.data.status==200){
                that.$message({
                  message: data.data.data,
                  offset: 60,
                  showClose: true,
                  center: true,
                  type: 'success'
                })
              }else{
                that.$message.error({
                  offset: 60,
                  center: true,
                  showClose: true,
                  message: data.data.data
                })
              }
            })
          },
          // 跳转到购物车界面
          to_shopping_car(){
            this.$router.push({name: 'shopping_car'})
          }
        },
        mounted(){
          this.get_goods();
          this.get_courses();
          this.get_coupons();
        }
    }
</script>

<style scoped>
  .shopping_car{
    z-index: 10000;
    display: inline-block;
    height: 50px;
    width: 150px;
    background-color: red;
    line-height: 50px;
    text-align: center;
    position: fixed;
    right: 0;
    top: 50%;
    margin-top: -52px;
    color: white;
    border-radius: 6px;
    cursor: pointer;
  }

  .coupon{
    z-index: 10000;
    display: inline-block;
    height: 50px;
    width: 150px;
    background-color: red;
    line-height: 50px;
    text-align: center;
    position: fixed;
    right: 0;
    top: 50%;
    color: white;
    border-radius: 6px;
    cursor: pointer;
  }

  .el-row {
  margin-bottom: 20px;
}
  .el-row:last-child {
    margin-bottom: 0;
  }


.footer{
  margin-top: 100px;
  bottom: 0;
  width: 100%;
  height: 120px;
  background-color: #333333;
  color: white;
  text-align: center;
  padding-top: 15px;
}

.footer div{
  margin-top: 10px;
}

.round-img{
  text-align: center;
  width: 70%;
  margin-left: 300px;
  margin-top: 40px;
}
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
.center{
  text-align: center
}

.title-background{
  display: inline-block;
  height: 100px;
  background-color: yellow;
  width: 350px;
  margin-top: -5px;
  text-align: center;
  border-radius: 5px;
}
.title{
  text-align: center;
  font-size: 36px;
  font-weight: 400;
  margin-top: 20px;
}
.company-intro{
  font-size: 20px;
  display: inline-block;
}
.company-intro div{
  margin-top: 10px;
}
.font-bolder{
  font-weight: bolder
}

  .brief {
    font-size: 13px;
    color: #999;
  }
  .type {
    font-size: 13px;
    color: #3a8ee6;
    margin-left: 10px;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    display: block;
  }

  .yellow{
    height:33px;
    width:100%;
    background-color: yellow;
    display: inline-block;
    margin-top: 40px;
  }
</style>
