<template>

  <el-row :gutter="20" style="margin-top: 100px;">

    <el-col :span="6">
      <div class="grid-content bg-purple">
        <el-button type="primary" style="float:right;margin-top:13px;" @click="back()">>>返回</el-button>
      </div>
    </el-col>

    <el-col :span="12">
      <div class="grid-content bg-purple">
        <el-table :data="tableData" stripe style="width: 100%">
          <el-table-column prop="title" label="标题" width="180"></el-table-column>
          <el-table-column prop="create_time" label="创建时间" width="180"></el-table-column>
          <el-table-column prop="like_count" label="点赞数" width="180"></el-table-column>
          <el-table-column prop="comment_count" label="评论数" width="180"></el-table-column>
          <el-table-column fixed="right" label="操作" width="110">
            <template slot-scope="scope">
              <el-button @click="to_edit_one_article(scope.row.id)" type="text" size="small">编辑</el-button>
              <el-button @click="confirm_delete_article(scope.row.id)" type="text" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!--确认删除-->
        <el-dialog title="提示" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
          <span>是否确认删除？</span>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="delete_article">确 定</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>

</template>

<script>
    export default {
        name: "edit-article",
        data(){
          return {
            tableData: [],
            dialogVisible: false,
            choice: 0,  // 选择的文章id
          }
        },
        methods:{
          // 返回个人博客
          back(){
            this.$router.push({name: 'one_blog', params: {username: this.$store.state.user}})
          },
          // 跳转到编辑文章页面
          to_edit_one_article(id){
            this.$router.push({name: 'edit_one_article', params: {id: id}})
          },
          // 确认是否删除文章
          confirm_delete_article(id){
            this.dialogVisible = true;
            this.choice = id;
          },
          // 删除文章
          delete_article(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/blog/articles/' + that.$store.state.user_id + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: "delete",
              data: {article_id: that.choice}
            }).then(function(data){
              that.dialogVisible = false;
              if(data.data.status==200){
                that.$message({
                  message: "删除成功",
                  center: true,
                  showClose: true,
                  offset: 60,
                  type: 'success'
                })
              }else{
                that.$message.error({
                  message: data.data.data,
                  center: true,
                  showClose: true,
                  offset: 60,
                })
              }
            })
          }
        },
        mounted(){
          let that = this;
          this.$axios.request({
            url: 'http://' + that.$store.state.host + ':8000/api/blog/articles/' + that.$store.state.user_id + '/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
            method: "get",
          }).then(function(data){
            if(data.data.status==200){
              that.tableData = data.data.articles;
            }
          })
        },
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
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }

</style>
