<template>
    <div style="margin-top: 50px;">
      <el-row :gutter="20">
        <el-col :span="6">
          <div style="clear:both"><el-button type="primary" style="float: right;margin-top: 30px;" @click="back('one_blog')">>> 个人博客</el-button></div>
          <div style="clear:both"><el-button type="primary" style="float: right;margin-top: 10px;" @click="back('blog')">>> 博客首页</el-button></div>
          <div style="clear:both"><el-button type="success" style="float: right;margin-top: 10px;" @click="speak">朗读</el-button></div>

        </el-col>
        <el-col :span="12">
          <div class="grid-content bg-purple">
            <el-card class="box-card outer-box">
              <div class="text">

                <!--左侧文章详情-->
                <el-col :span="18" class="item">

                  <!--文章-->
                  <h2 class="article_title" style="">
                    {{article_detail.article.title}}

                  </h2>
                  <hr>
                  <div v-html="article_detail.content"></div>
                  <div class="category">
                    分类：<span style="border-bottom: 1px #6e6e6e dashed">{{article_detail.article.category}}</span>
                  </div>

                  <!--点赞、分享-->
                  <div class="share-like">
                    <div class="share">分享到：<share :config="config" style="display: inline-block"></share></div>

                    <div class="like" @click="like">
                      <div class="like_count">{{article_detail.article.like_count}}</div>
                      <div class="recommend">
                        <div v-if="is_like"><i class="el-icon-star-on"></i>推荐</div>
                        <div v-else><i class="el-icon-star-off"></i>推荐</div>
                      </div>
                    </div>
                  </div>
                  <div class="hide" ref="radio_div" style="margin-top: 50px; margin-left: -10px;"><audio :src="radio_src" controls autoplay></audio></div>
                  <!--评论-->

                </el-col>

                <!--右侧作者信息-->
                <el-col :span="6" style="margin-bottom: 20px;">
                  <div class="info-head" style="margin-top: 60px;">作者信息</div>
                  <div class="info-body">
                    <div>
                      用户名：
                      <span style="color: #3a8ee6; cursor: pointer;" @click="to_one_blog(article_detail.author.username)">
                        {{article_detail.article.author}}
                      </span>
                    </div>
                    <div>签名：{{article_detail.author.sign}}</div>
                  </div>

                  <div class="info-head" style="">点赞排行</div>
                  <div class="info-body">
                    <div v-for="article in like_articles" :key="article">
                      {{article.title}}（{{article.like_count}}）
                    </div>
                  </div>

                  <div class="info-head">文章分类</div>
                  <div class="info-body">
                    <div v-for="category in categories" :key="category">
                      {{category.title}}（{{category.count}}）
                    </div>
                  </div>
                </el-col>

              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
</template>

<script>
    export default {
        name: "article-detail",
        data(){
          return {
            article_detail: {},
            like_articles: [],
            categories: [],
            is_like: null,
            config: {
              sites: ['qzone', 'qq', 'weibo','wechat'],
            },
            radio_src: "http://" + this.$store.state.host + ':8000/'
          }
        },
        computed:{

        },
        methods:{
          // 点赞
          like(){
            let that = this;
            this.$axios.request({
              url: "http://" + that.$store.state.host + ":8000/api/blog/like/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
              method: "post",
              data: {"article_id": that.article_detail.article.id}
            }).then(function(data){
              if(data.data.status==200){
                that.article_detail.article.like_count += 1;
                that.is_like = data.data.data;
              }else if(data.data.status==430){
                that.article_detail.article.like_count -= 1;
                that.is_like = data.data.data;
              }
            })
          },
          // 跳转到某个用户的博客
          to_one_blog(username){
            this.$router.push({name: "one_blog", params:{username: username}});
          },
          // 返回
          back(name){
            if(name=='one_blog'){
              this.$router.push({name:  name, params: {username: this.$store.state.user}})
            }
            else{
              this.$router.push({name:  name})
            }
          },
          // 朗读文章
          speak(){
            this.$message({
              message: "请稍等",
              showClose: true,
              center: true,
              offset: 60,
            });
            let article_id = this.$route.params.id;
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/blog/radio/' + article_id + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: 'get',
            }).then(function(data){
              console.log(data.data)
              that.radio_src += data.data.data;
              that.$refs.radio_div.classList.add('show')
            })
          }
        },
        mounted(){
          let that = this;
          this.$axios.request({
            url: "http://" + that.$store.state.host + ":8000/api/blog/article_detail/" + that.$route.params.id + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
            method: "get",
          }).then(function(data){
            if(data.data.status==200){
              that.article_detail = data.data.article_detail;
              that.like_articles = data.data.like_articles;
              that.categories = data.data.categories;
              that.is_like = data.data.is_like;
            }
          })
        }
    }
</script>

<style scoped>
  .el-row {
    margin-bottom: 20px;}

    .el-row:last-child {
      margin-bottom: 0;
    }

  .el-col {
    border-radius: 4px;
  }

  .bg-purple {
    background: #d3dce6;
  }

  .grid-content {
    border-radius: 4px;
  }

    .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 25px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .article_title{
    border-left: 10px #3a8ee6 solid;
    padding-left: 10px;
  }

.info-head{
  border:1px #cccccc solid;
  background-color: #f0f0f0;
  padding: 5px 10px;
  font-weight: bold;
  margin-top: 20px;
}

  .info-body{
    font-size: 12px;
    margin-left: 10px;
    margin-top: 20px;
  }
  .info-body div{
    margin-top: 10px;
  }
  .category{
    margin-top: 50px;
  }
  .share-like{
    margin-top: 20px;
  }
  .share{
    font-size: 20px;
    display: inline-block;
  }
.like{
  float: right;
  margin-right: 50px;
  width: 50px;

  background-color: #fff0b4;
  text-align: center;
  cursor: pointer;
}
.like_count{
  line-height: 36px;
}
.recommend{
  height: 23px;
  background-color: #d6fcff;
  color: #3a8ee6;
  text-align: center;
  line-height: 23px;
}
.hide{
  display: none
}
.show{
  display: inline;
}
</style>
