<template>
    <div style="background-color: #e5e9f2;min-height: 820px;">
      <el-row :gutter="20">
        <!--左侧栏-->
        <el-col :span="4" :offset="3">
          <div class="grid-content">

            <!--作者文章点赞排行榜-->
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span class="card-head-left">文章点赞榜</span>
                <span class="card-head-right">被赞总数 {{like_count}}</span>
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

            <!--常用操作-->
            <el-card class="box-card" style="margin-top: 50px">
              <div slot="header" class="clearfix">
                <span class="card-head-left">常用操作</span>
              </div>
              <div v-if="author_name = $store.state.user">
                <div class="text item hover-hand" @click="to_add_article">>>写新文章</div>
                <div class="text item hover-hand" @click="to_edit_article">>>编辑文章</div>
                <div class="text item hover-hand" @click="to_edit_category">>>编辑分类</div>
              </div>

              <div v-else>
                <div class="text item">>>返回博客首页</div>
              </div>
            </el-card>

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
                    <span style="font-size: 14px; color: #3a8ee6; cursor: pointer;" @click="to_one_blog(article.author.id)">{{article.author.username}}</span>
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
                  还没有发表过文章，快来发表你的第一篇文章吧！
                </div>
              </el-card>
            </div>

          </div>
        </el-col>

        <!--右侧栏-->
        <el-col :span="4">
          <div class="grid-content">

            <!--作者信息-->
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span v-text="$store.state.user" class="card-head-left"></span>
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

            <!--文章分类列表-->
            <el-card class="box-card" style="margin-top: 50px">
              <div slot="header" class="clearfix">
                <span  class="card-head-left">文章分类</span>
                <el-button style="float: right; padding: 3px 0" type="text" @click="centerDialogVisible = true">添加分类</el-button>
              </div>
              <div v-if="categories">
                <div class="text item">全部</div>
                <div v-for="category in categories" :key="categories" class="text item">
                  {{category.title}}（{{category.count}}）
                </div>
              </div>
              <div v-else>
                还没有创建过文章分类。
              </div>
            </el-card>

            <!--添加分类框-->
            <el-dialog title="添加分类" :visible.sync="centerDialogVisible" width="30%" center>
              <el-form ref="form" :model="form" label-width="90px">
                <el-form-item label="分类名称：">
                  <el-input v-model="category_title" @focus="clearError"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="centerDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="add_category">确 定</el-button>
                <span ref="category_error" class="error_info"></span>
              </span>
            </el-dialog>

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
            author_name: "",

          }
        },
        methods:{
          // 跳转到文章详情界面
          article_detail(id){
            this.$router.push({name: "article_detail", params: {id: id}})
          },
          // 添加分类
          add_category(){
            let that = this;
            if(that.category_title==""){
              console.log(123)
              that.$refs.category_error.innerText = "请输入分类名";
            }else{
              this.$axios.request({
                url: "http://" + that.$store.state.host + ":8000/api/blog/category/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
                method: "post",
                data: {"title": that.category_title},
              }).then(function(data){
                if(data.data.status==200){
                  that.centerDialogVisible = false;
                  that.categories = data.data.categories;
                  that.$message({
                    message: data.data.data,
                    type: "success",
                    center: true,
                    offset: 60,
                    showClose: true,
                  });
                }else if(data.data.status==431){
                  that.$refs.category_error.innerText = "该分类已存在"
                }
              })
            }
          },
          // 清除错误信息
          clearError(){
            this.$refs.category_error.innerText = "";
          },
          // 跳转到写新文章的页面
          to_add_article(){
            this.$router.push({name: "write_article"})
          },
          // 跳转到编辑文章页面
          to_edit_article(){
            this.$router.push({name: 'edit_article'})
          },
          // 跳转到编辑分类页面
          to_edit_category(){
            this.$router.push({name: 'edit_category'})
          }
        },
        mounted(){
          let that = this;
          this.$axios.request({
            url: 'http://' + that.$store.state.host + ':8000/api/blog/articles/' + that.$store.state.user_id + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
            method: "get",
          }).then(function(data){
            if(data.data.status==200){
              that.articles = data.data.articles;
              that.likes = data.data.likes;
              that.categories = data.data.categories;
              that.sign = data.data.sign;
              that.like_count = data.data.like_count;
              that.article_count = data.data.article_count;
              that.author_id = data.data.author_id;
            }else if(data.data.status==430){
              that.has_articles = false;
            }
          })
        },

    }
</script>

<style scoped>
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
    .bg-purple {
    background: #d3dce6;
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
  .card-head-left{
    color: #3a8ee6
  }
  .card-head-right{
    float: right;
    font-size: 16px;
    color: #409eff;
  }
  .hover-hand{
    cursor: pointer;
  }
</style>
