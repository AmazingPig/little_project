<template>
  <div>
      <LeftMenu></LeftMenu>

      <div class="right">
        <el-card class="box-card">
          <div slot="header" class="clearfix head">
            <span>成绩管理</span>
          </div>
          <div class="text item">
            <!--操作-->
            <div>
              <!--批量操作-->
              <el-select v-model="multi" placeholder="请选择" style="margin-bottom: 10px">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
              <el-button type="primary" @click="multi_manage">批量操作</el-button>

              <!--添加按钮-->
              <el-button type="primary" class="add" @click="addForm = true">添加成绩</el-button>
            </div>
            <!--表格-->
            <el-table :data="grades" border style="width: 100%" @selection-change="handleSelectionChange">
              <el-table-column type="selection" label="选择" width="60"></el-table-column>
              <el-table-column prop="course_title" label="课程名" width="120"></el-table-column>
              <el-table-column prop="student_name" label="学生" width="120"></el-table-column>
              <el-table-column prop="grade" label="成绩" width="120"></el-table-column>
              <el-table-column prop="note" label="评语" width="200"></el-table-column>
              <el-table-column fixed="right" label="操作" width="150">
                <template slot-scope="scope">
                  <el-button type="text" size="small" @click="to_edit(scope.row)">编辑</el-button>
                  <el-button type="text" size="small" @click="confirm_del(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

          </div>
        </el-card>
      </div>

      <!--确认删除-->
      <el-dialog title="提示" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
        <span>是否确认删除？</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="del">确 定</el-button>
        </span>
      </el-dialog>

      <!--添加/编辑成绩-->
      <el-dialog :title="get_title" :visible.sync="addForm" width="30%" center="true">
        <el-form :model="form" label-width="80px">
          <el-form-item label="学生">
            <el-select v-model="form.student" placeholder="请选择学生" @focus="clearError">
              <el-option label="---------" :value="0"></el-option>
              <div v-for="(student,index) in students">
                <el-option :label="student.name" :value="student.id"></el-option>
              </div>
            </el-select>
          </el-form-item>
          <el-form-item label="课程">
            <el-select v-model="form.course" placeholder="请选择课程" @focus="clearError">
              <el-option label="---------" :value="0"></el-option>
              <div v-for="(course,index) in courses">
                <el-option :label="course.title" :value="course.id"></el-option>
              </div>
            </el-select>
          </el-form-item>
          <el-form-item label="成绩">
            <el-input v-model="form.grade" autocomplete="off" @focus="clearError"></el-input>
          </el-form-item>
          <el-form-item label="评语">
            <el-input v-model="form.note" autocomplete="off" @focus="clearError"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="clearForm">取 消</el-button>
          <el-button type="primary" @click="submit">确 定</el-button>
          <span class="error_info" ref="error_info"></span>
        </div>
      </el-dialog>


  </div>
</template>

<script>
    import LeftMenu from './index'
    export default {
        name: "grade",
        data(){
          return {
            grades: [],
            students: [],
            courses: [],
            multipleSelection: [],
            dialogVisible: false,
            addForm: false,
            is_edit: false,
            add_or_edit: "",
            choice_id: [],
            form: {
              student: "",
              course: "",
              grade: "",
              note: "",
            },
            options:[
              {label: "---请选择---", value: ""},
              {label: "删除", value: "multi_del"}
            ],
            multi: "",
          }
        },
        computed:{
          get_title(){
            if(this.is_edit){
              return "编辑成绩记录"
            }else{
              return "添加成绩记录"
            }
          },
          course_id(){
            if(this.$route.query.course_id){
              return this.$route.query.course_id
            }else{
              return 0
            }
          },
          student_id(){
            if(this.$route.query.student_id){
              return this.$route.query.student_id
            }else{
              return 0
            }
          }
        },
        methods:{
          handleSelectionChange(val) {
            this.multipleSelection = val;
          },

          // 获取课程信息
          get_grades(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/school/grades/?course_id=' + that.course_id + '&student_id=' + that.student_id + '&username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: 'get'
            }).then(function(data){
              that.grades = data.data.grades;
              that.students = data.data.students;
              that.courses = data.data.courses;
            })
          },
          // 弹出确认删除框
          confirm_del(id){
            this.choice_id = [];
            this.choice_id.push(id);
            this.dialogVisible = true;
          },
          // 删除成绩
          del(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/school/grades/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: 'delete',
              data: {id: that.choice_id}
            }).then(function(data){
              that.dialogVisible = false;
              if(data.data.status==200){
                that.get_grades();
                that.$message({
                  type: 'success',
                  showClose: true,
                  center: true,
                  message: data.data.data,
                  offset: 60
                })
              }else{
                that.$message.error({
                  message: data.data.data,
                  showClose: true,
                  center: true,
                  offset: 60
                })
              }
            })
          },
          // 添加成绩
          add_grade(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/school/grades/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: 'post',
              data: that.form,
            }).then(function(data){
              if(data.data.status==200){
                that.addForm = false;
                that.form = {};
                that.get_grades();
                that.$message({
                  type: 'success',
                  showClose: true,
                  center: true,
                  message: data.data.data,
                  offset: 60
                })
              }else{
                that.$refs.error_info.innerText = "请输入正确格式的信息"
              }
            })
          },
          // 弹出编辑框
          to_edit(form){
            this.is_edit = true;
            this.addForm = true;
            this.form = {...form};

          },
          // 提交编辑信息
          edit_grade(){
            let that = this;
            this.$axios.request({
              url: 'http://' + that.$store.state.host + ':8000/api/school/grades/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
              method: 'put',
              data: that.form,
            }).then(function(data){
              if(data.data.status==200){
                that.addForm = false;
                that.is_edit = false;
                that.form = {};
                that.get_grades();
                that.$message({
                  type: 'success',
                  showClose: true,
                  center: true,
                  message: data.data.data,
                  offset: 60
                })
              }else{
                that.$refs.error_info.innerText = "请输入正确格式的信息"
              }
            })
          },
          // 清除错误信息
          clearError(){
            this.$refs.error_info.innerText = ""
          },
          // 清空form表单
          clearForm(){
            this.form = {};
            this.addForm = false;
            this.is_edit = false;
          },
          // 点击确定
          submit(){
            if(this.is_edit){
              this.edit_grade()
            }else{
              this.add_grade()
            }
          },
          // 批量操作
          multi_manage() {
            for(let i=0; i<this.multipleSelection.length; i++){
              this.choice_id.push(this.multipleSelection[i].id)
            }
            if(this.multi=="multi_del"){
              // 批量删除
              this.del()
            }
          }
        },

        components:{
          LeftMenu
        },
        mounted(){
          this.get_grades()
        }

    }
</script>

<style scoped>
.right{
  display: inline-block;
  float: right;
  margin-right: 300px;
  margin-top: 100px;
}
.head{
  text-align: center;
  font-size: 25px;
  color: #66b1ff;
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
  width: 1000px;
}
.add{
  float: right;
  margin-bottom: 10px;
}
.error_info{
  margin-left: 20px;
  color:red;
}
</style>
