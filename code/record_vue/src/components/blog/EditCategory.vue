<template>
    <div>
      <el-row :gutter="20" style="margin-top: 100px;">
        <el-col :span="6">
          <el-button type="primary" style="float: right; margin-top:15px;" @click="back">>>返回</el-button>
        </el-col>

        <el-col :span="12">
          <div class="grid-content bg-purple">
            <el-table :data="tableData" stripe style="width: 100%">
              <el-table-column prop="title" label="标题" width="180"></el-table-column>
              <el-table-column prop="count" label="文章数" width="600"></el-table-column>
              <el-table-column fixed="right" label="操作" width="120">
                <template slot-scope="scope">
                  <el-button @click="to_edit_category(scope.row.id, scope.row.title)" type="text" size="small">编辑</el-button>
                  <el-button @click="confirm_delete_category(scope.row.id)" type="text" size="small">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <!--确认删除-->
            <el-dialog title="提示" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
              <span>是否确认删除？</span>
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="delete_category">确 定</el-button>
              </span>
            </el-dialog>

            <!--编辑分类-->
            <el-dialog title="编辑分类" :visible.sync="centerDialogVisible" width="30%" center>
              <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="分类名：">
                  <el-input v-model="model_title" @focus="clearError"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button @click="centerDialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="edit_category">确 定</el-button>
                <span class="error_info" ref="error_info"></span>
              </span>
            </el-dialog>
          </div>
        </el-col>
      </el-row>
    </div>
</template>

<script>
    export default {
        name: "edit-category",
        data(){
          return {
            tableData: [],
            dialogVisible: false,
            centerDialogVisible: false,
            choice: 0,  // 选择的分类id
            category_title: "",  // 表示编辑前的值
            model_title: ""  // 获取输入的值
          }
        },
        methods:{
          // 返回个人博客页
          back(){
            this.$router.push({name: 'one_blog', params: {id: this.$store.state.user_id}})
          },
          // 跳出编辑分类框
          to_edit_category(id, title){
            this.centerDialogVisible = true;
            this.category_title = title;
            this.model_title = title;
            this.choice = id;
          },
          // 提交编辑分类
          edit_category(){
            if(this.model_title==""){
              this.$refs.error_info.innerText = "请输入分类名"
            }else if(this.model_title==this.category_title){
              this.centerDialogVisible = false;
            }else{
              let that = this;
              this.$axios.request({
                url: "http://" + that.$store.state.host + ":8000/api/blog/category/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
                method: "put",
                data: {category_id: that.choice, category_title: that.model_title}
              }).then(function(data){
                if(data.data.status==200){
                  that.centerDialogVisible = false;
                  that.$message({
                    message: "编辑成功",
                    type: "success",
                    center: true,
                    offset: 60,
                    showClose: true
                  })
                }else{
                  that.$message.error({
                    message: "编辑成功",
                    center: true,
                    offset: 60,
                    showClose: true
                  })
                }
              })
            }
          },
          // 确认是否删除分类
          confirm_delete_category(id){
            this.dialogVisible = true;
            this.choice = id
          },
          // 删除分类
          delete_category(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/blog/category/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: "delete",
              data: {category_id: that.choice}
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
          },
          // 清除错误信息
          clearError(){
            this.$refs.error_info.innerText = ""
          }
        },
        mounted(){
          let that = this;
          this.$axios.request({
            url: "http://" + that.$store.state.host + ":8000/api/blog/category/?username=" + that.$store.state.user + "&token=" + that.$store.state.token,
            method: "get",
          }).then(function(data){
            that.tableData = data.data.data;
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
    margin-left: 20px;
    color: red;
    font-size: 18px;
    margin-right: 20px;
  }
</style>
