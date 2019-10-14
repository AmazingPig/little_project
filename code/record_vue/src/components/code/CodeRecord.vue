<template>
  <div style="position: relative;">

    <div class="total_code">
      <span v-text="$store.state.user"></span>
      的代码总量为：
      <span v-text="total_count_latest"></span>
    </div>

    <div class="code_table">
      <el-button type="primary" @click="for_file">上传代码</el-button>
      <span style="color:orangered">（请选择zip格式的压缩文件）</span>
      <form>
        <input id="file" type="file" ref="file" @change="upload_file">
      </form>
      <el-table :data="tableData" style="width: 100%" max-height="500" border>
        <el-table-column fixed prop="date" label="日期" width="150"></el-table-column>
        <el-table-column prop="user" label="用户" width="120"></el-table-column>
        <el-table-column prop="title" label="标题" width="200"></el-table-column>
        <el-table-column prop="count" label="代码行数" width="120"></el-table-column>
        <el-table-column prop="manage" label="操作" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="small">
              <span @click="download_file(scope.$index, tableData)"><el-button size="mini" round=true type="primary">下载</el-button></span>
              <span @click="del_file(scope.$index, tableData)"><el-button size="mini" round=true type="primary">删除</el-button></span>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

    </div>

    <Charts :date_counts="date_counts" :date_list="date_list"></Charts>

</div>
</template>

<script>
  import Charts from './Charts'
  export default {
    name: "code-record",
    components:{
      Charts
    },
    data() {
      return {
        tableData: [],
        total_count: 0,
        date_counts: [],
        date_list: [],
      }
    },
    computed:{
      // 实时监测代码总量
      total_count_latest(){
        return this.total_count;
      },
    },
    methods:{
      // 从后端获取代码记录
      get_record(){
        let that = this;
        this.$axios.request({
           url: 'http://' + that.$store.state.host + ':8000/api/code/records/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
           method: 'get',
        }).then(function(data){
          if(data.data.status==200) {
            that.tableData = data.data.data;
            that.total_count = data.data.total_count;
            that.date_counts = data.data.date_counts;
            that.date_list = data.data.date_list;
          }
        })
      },
      // 点击按钮触发选择文件按钮
      for_file(){
        this.$refs.file.click();
      },
      // 上传文件到后端
      upload_file(){
        let that = this;
        let formData = new FormData();
        formData.append("file", this.$refs.file.files[0]);
        this.$axios.request({
          url: 'http://' + that.$store.state.host + ':8000/api/code/records/?username=' + that.$store.state.user + '&token=' + that.$store.state.token,
          method: 'post',
          data: formData
        }).then(function(data){
          if(data.data.status==200){
            that.get_record();
            that.$message({
              message: "上传成功",
              type: "success",
              center: true,
              offset: 60,
              showClose: true,
            });
          }else{
            that.$message({
              message: data.data.data,
              type: "success",
              center: true,
              offset: 60,
              showClose: true,
            });
          }
        })
      },
      // 删除文件
      del_file(index, obj){
        let is_del = confirm("是否确定删除该文件？");
        if(is_del){
          let that = this;
          this.$axios.request({
            url: "http://" + that.$store.state.host + ":8000/api/code/records/?username=" + that.$store.state.user + '&token=' + that.$store.state.token,
            method: "delete",
            data: {id: obj[index]["id"]},
          }).then(function(data){
            if(data.data.status==200){
              that.get_record();
              that.$message({
                message: "删除成功",
                type: "success",
                center: true,
                offset: 60,
                showClose: true,
              });
            }else{
              that.$message({
                message: data.data.data,
                type: "success",
                center: true,
                offset: 60,
                showClose: true,
              });
            }
          })
        }
      },
      // 下载文件
      download_file(index, obj){
        let that = this;
        this.$axios.request({
          url: "http://" + that.$store.state.host + ":8000/api/code/get_code_file/?id=" + parseInt(obj[index]["id"]) + "&username=" + that.$store.state.user + "&token=" + that.$store.state.token,
          method: "get",
        }).then(function(data){
          if(data.data.status==200){
            let tag_a = document.createElement("a");
            tag_a.href = "http://127.0.0.1:8000/" + data.data.data;
            tag_a.click();
          }else{
            alert(data.data.status);
          }
        })
      },
    },
    mounted(){
      this.get_record();
    }
  }


</script>

<style scoped>

.code_table{
  width: 741px;
  margin-top: 100px;
  margin-left: 600px;
}
.el-table{
  margin-top: 10px;
}
  #file{
    display: none;
  }
  .total_code{
    display: inline-block;
    font-size: 30px;
    color: #409EFF;
    position: absolute;
    top: -2px;
    left: 1000px;
  }

</style>
