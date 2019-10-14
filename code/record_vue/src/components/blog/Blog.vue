<template>
    <div style="background-color: #e5e9f2;min-height: 820px;">
      <el-row :gutter="20">
        <!--左侧栏-->
        <el-col :span="4" :offset="3">
          <div class="grid-content">

            <!--文章点赞排行榜-->
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span style="color: #3a8ee6">文章点赞榜</span>
              </div>
              <div v-if="likes">
                <div v-for="article in likes" :key="likes" class="text item">
                  <span @click="article_detail(article.id)" class="hover-hand">{{article.title}}（{{article.like_count}}）</span>
                </div>
              </div>
              <div v-else>
                <div>还没有发表过文章。</div>
              </div>
            </el-card>

            <!--广告-->
            <div ref="adv1">
              <el-card class="box-card" style="margin-top: 50px;" :body-style="{ padding: '10px' }">
                <div slot="header" class="clearfix">
                  <span>广告</span>
                  <el-button style="float: right; padding: 3px 0" type="text" @click="close_adv1"><span style="font-size: 16px;">关闭</span></el-button>
                </div>
                <div class="text item">
                <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
                <div style="padding-left: 14px; padding-right: 14px; padding-top: 14px; padding-bottom: -20px;">
                  <span>好吃的汉堡</span>
                  <el-button type="text" class="button">操作按钮</el-button>
                </div>
                </div>
              </el-card>
            </div>

          </div>
        </el-col>

        <!--文章列表-->
        <el-col :span="10">
          <div class="grid-content bg-purple-light">
            <div v-if="has_articles">
              <el-card v-for="article in articles" :key="article" class="box-card" shadow="hover">
                <div slot="header" class="clearfix">
                  <span class="article-title" @click="article_detail(article.id)">{{article.title}}</span>
                  <el-button style="float: right; padding: 3px 0" type="text" @click="article_detail(article.id)">查看详情</el-button>
                </div>
                <div class="text item">
                  <div class="article-brief" @click="article_detail(article.id)" v-html="article.brief"></div>
                  <div class="article-footer">
                    <span style="font-size: 14px; color: #3a8ee6; cursor: pointer;" @click="to_one_blog(article.author.username)">{{article.author.username}}</span>
                    <span>发布于：{{article.create_time}}</span>
                    <span>点赞（{{article.like_count}}）</span>
                    <span>评论（{{article.comment_count}}）</span>
                  </div>
                </div>
              </el-card>
            </div>

            <div v-else>
              <el-card class="box-card">
                <div slot="header" class="clearfix">
                  <span class="article-title">欢迎~~</span>
                </div>
                <div class="text item">
                  还没有人发表过文章，快来发表第一篇文章吧！
                </div>
              </el-card>
            </div>

          </div>
        </el-col>

        <!--右侧栏-->
        <el-col :span="4">
          <div class="grid-content">

            <!--用户信息-->
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span v-text="$store.state.user" style="color: #3a8ee6; cursor: pointer" @click="to_one_blog($store.state.user)"></span>
                <el-button style="float: right; padding: 3px 0" type="text" @click="to_one_blog($store.state.user)">我的博客</el-button>
              </div>
              <div class="text item">文章数：{{article_count}}</div>
              <div class="text item">被赞数：{{like_count}}</div>
              <div v-if="sign" class="text item">
                签名：{{sign}}
              </div>
              <div v-else class="text item">
                没有签名。
              </div>
            </el-card>

            <!--广告-->
            <div ref="adv2">
              <el-card class="box-card" style="margin-top: 50px;" :body-style="{ padding: '10px' }">
                <div slot="header" class="clearfix">
                  <span>广告</span>
                  <el-button style="float: right; padding: 3px 0" type="text" @click="close_adv2"><span style="font-size: 16px;">关闭</span></el-button>
                </div>
                <div class="text item">
                <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" class="image">
                <div style="padding-left: 14px; padding-right: 14px; padding-top: 14px; padding-bottom: -20px;">
                  <span>好吃的汉堡</span>
                  <el-button type="text" class="button">操作按钮</el-button>
                </div>
                </div>
              </el-card>
            </div>

          </div>
        </el-col>
      </el-row>
    </div>
</template>

<script>
    export default {
        name: "blog",
        data(){
          return {
            has_articles: true,
            articles:[],
            likes: [],
            categories: [],
            sign: "",
            like_count: 0,
            article_count: 0,
            centerDialogVisible: false,
            category_title: "",
          }
        },
        methods:{
          // 跳转到文章详情界面
          article_detail(id){
            this.$router.push({name: "article_detail", params: {id: id}})
          },
          // 跳转到某个用户的博客
          to_one_blog(username){
            this.$router.push({name: "one_blog", params:{username: username}});
          },
          // 关闭广告
          close_adv1(){
            this.$refs.adv1.style.display='none';
          },
          close_adv2(){
            this.$refs.adv2.style.display='none';
          },
          // 清除错误信息
          clearError(){
            this.$refs.category_error.innerText = "";
          }
        },
        mounted(){
          let that = this;
          this.$axios.request({
            url: 'http://' + that.$store.state.host + ':8000/api/blog/articles/' + 0 + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
            method: "get",
          }).then(function(data){
            if(data.data.status==200){
              that.articles = data.data.articles;
              that.likes = data.data.likes;
              that.categories = data.data.categories;
              that.sign = data.data.sign;
              that.like_count = data.data.like_count;
              that.article_count = data.data.article_count;
            }else if(data.data.status==430){
              that.has_articles = false;
            }
          })
        },

    }
</script>

<style scoped>
  a{
    text-decoration: none;
    color: #3a8ee6;
  }
.el-row {
  margin-bottom: 20px;
  margin-top: 10px;
}
.el-row:last-child {
  margin-bottom: 0;
}
    .el-col {
    border-radius: 4px;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
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
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }
  .box-card{
    margin-top: 20px;
  }
.article-footer{
  margin-top: 20px;
  margin-bottom: -20px;
  font-size:12px;
}
.article-footer span{
  margin-right: 15px;
}
.article-title{
  color: #3a8ee6;
  font-size: 17px;
  cursor: pointer;
}
  .article-brief{
    font-size: 16px;
    cursor: pointer;
  }
  .error_info{
    color: red;
    font-size: 14px;
    margin-left: 10px;
  }
  .hover-hand{
    cursor: pointer;
  }
</style>
