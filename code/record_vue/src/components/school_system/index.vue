<template>
    <div>
      <div class="left-menu">
        <ul>
          <li ref="cls"><router-link to="/school_system/classes">班级管理</router-link></li>
          <li ref="student"><router-link to="/school_system/students">学生管理</router-link></li>
          <li ref="course"><router-link to="/school_system/courses">课程管理</router-link></li>
          <li ref="teacher"><router-link to="/school_system/teachers">老师管理</router-link></li>
        </ul>
      </div>


    </div>
</template>

<script>

    export default {
        name: "index",
        mounted(){
          let path = this.$route.path;
          if(path=='/school_system/students'){
            this.$refs.student.classList.add('active')
          }else if(path=='/school_system/classes'){
            this.$refs.cls.classList.add('active')
          }else if(path=='/school_system/teachers'){
            this.$refs.teacher.classList.add('active')
          }else if(path=='/school_system/courses'){
            this.$refs.course.classList.add('active')
          }else if(path=='/school_system/grades'){
            this.$refs.course.classList.add('active')
          }
        }
    }
</script>

<style scoped>
.left-menu{
  position:fixed;
  top:0;
  left:0;
  width: 250px;
  height: 100%;
  margin-top: 70px;
  margin-left: 10px;
  background-color: #e5e9f2;
  display: inline-block;
}
ul{
  list-style: none;
  margin-top: 40px;
}
ul li{
  float: right;
  clear: both;
  margin-bottom: 30px;
  margin-right: -80px;
  color: #66b1ff;
  font-size: 18px;
  border-left: 5px #66b1ff solid;
  width: 100%;
  padding-left: 115px;
  cursor:pointer
}
a{
  text-decoration: none;
}
a:visited{
  color: #66b1ff;
}
a:hover{
  color: #3a8ee6;

}
.active{
  border-left: 5px red solid;

}

</style>
