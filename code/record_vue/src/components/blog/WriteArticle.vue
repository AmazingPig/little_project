<template>
    <div>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-button type="primary" style="float: right;margin-top: 100px;" @click="back()">>>返回</el-button>
        </el-col>

        <el-col :span="12">
          <div class="grid-content">
            <!--标题-->
            <div class="title">
                <el-input placeholder="请输入内容" v-model="title" @focus="clearError">
                  <template slot="prepend">输入标题：</template>
                </el-input>
            </div>

            <!--文本编辑器-->
            <div id="editor"></div>

            <!--选择分类-->
            <el-form ref="form" :model="form" label-width="80px" style="float:left; margin-top: 10px;margin-left:-40px;">
                <el-form-item label="分类">
                  <el-select v-model="form.category" placeholder="请选择分类">
                    <div v-for="cat in category" :key="category">
                      <el-option :label="cat.title" :value="cat.id"></el-option>
                    </div>
                  </el-select>
                </el-form-item>
            </el-form>

            <!--提交-->
            <el-button type="primary" style="float:right;margin-top: 10px;" @click="add_article">提交</el-button>
            <span class="error_info" ref="error_info"></span>

          </div>
        </el-col>
      </el-row>
    </div>
</template>

<script>
  import wangEditor from 'wangeditor'
  export default {
    name: "write_article",
    data(){
      return {
        title: "",
        form: {
          category: '',
        },
        category: []
      }
    },
    methods:{
      // 返回个人博客
      back(){
        this.$router.push({name:  "one_blog", params: {username: this.$store.state.user}})
      },
      // 清除错误信息
      clearError(){
        this.$refs.error_info.innerText = ""
      },
      // 创建新文章
      add_article(){
        let content = this.editor.txt.html();  // 获取文章内容
        if(this.title==""){
          this.$refs.error_info.innerText = "请输入标题"
        }else if(content==""){
          this.$refs.error_info.innerText = "请输入内容"
        }else{
          let that = this;
          this.$axios.request({
            url: "http://" + that.$store.state.host + ":8000/api/blog/articles/" + that.$store.state.user_id + "/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
            method: "post",
            data: {title: that.title, content: content, category_id: that.form.category}
          }).then(function(data){
            if(data.data.status==200){
              that.$router.push({name: "one_blog", params: {username: that.$store.state.user}})
              that.$message({
                message: data.data.data,
                type: "success",
                center: true,
                offset: 60,
                showClose: true,
              })
            }else{
              that.$message.error({
                message: data.data.data,
                center: true,
                offset: 60,
                showClose: true
              })
            }
          })
        }
      },
    },
    mounted(){
      // 生成编辑器
      this.editor = new wangEditor('#editor');
      this.editor.create();

      // 获取分类
      let that = this;
      this.$axios.request({
        url: 'http://' + that.$store.state.host + ':8000/api/blog/category/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
        method: "get",
      }).then(function(data){
        if(data.data.status==200){
          that.category = data.data.data
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
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .title{
    margin-top: 100px;
  }
  .error_info{
    float: right;
    color: red;
    font-size: 18px;
    margin-right: 20px;
    margin-top: 18px;
  }
</style>
