import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/Home'
import CodeRecord from '../components/code/CodeRecord'
import Blog from '../components/blog/Blog'
import ArticleDetail from '../components/blog/ArticleDetail'
import OneBlog from '../components/blog/OneBlog'
import WriteArticle from '../components/blog/WriteArticle'
import EditArticle from '../components/blog/EditArticle'
import EditOneArticle from '../components/blog/EditOneArticle'
import EditCategory from '../components/blog/EditCategory'
import School from '../components/school_system/index'
import Student from '../components/school_system/Student'
import Class from '../components/school_system/Cls'
import Teacher from '../components/school_system/Teacher'
import Course from '../components/school_system/Course'
import Grade from '../components/school_system/Grade'
import PotteryIndex from '../components/pottery/Index'
import ShoppingCar from '../components/pottery/ShoppingCar'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      // 首页
      path: '/',
      name: 'home',
      component: Home
    },
    {
      // 代码记录页
      path: '/code/record',
      name: 'code_record',
      component: CodeRecord,
    },
    {
      // 博客页
      path: '/blog',
      name: 'blog',
      component: Blog,
    },
    {
      // 个人博客页
      path: '/blog/:username',
      name: 'one_blog',
      component: OneBlog,
    },
    {
      // 文章详细页
      path: '/blog/article_detail/:id',
      name: 'article_detail',
      component: ArticleDetail,
    },
    {
      // 写文章页
      path: '/blog/write_article',
      name: 'write_article',
      component: WriteArticle,
    },
    {
      // 选择编辑文章页
      path: '/blog/edit_article',
      name: 'edit_article',
      component: EditArticle
    },
    {
      // 编辑文章页
      path: '/blog/edit_article/:id',
      name: 'edit_one_article',
      component: EditOneArticle
    },
    {
      // 编辑分类页
      path: '/blog/edit_category',
      name: 'edit_category',
      component: EditCategory,
    },
    {
      // 学校管理系统
      path: '/school_system',
      name: 'school_system',
      component: School
    },
    {
      // 学生管理
      path: '/school_system/students',
      name: 'student',
      component: Student
    },
    {
      // 班级管理
      path: '/school_system/classes',
      name: 'class',
      component: Class,
    },
    {
      // 老师管理
      path: '/school_system/teachers',
      name: 'teacher',
      component: Teacher,
    },
    {
      //课程管理
      path: '/school_system/courses',
      name: 'course',
      component: Course
    },
    {
      // 成绩管理
      path: '/school_system/grades',
      name: 'grade',
      component: Grade
    },
    {
      // 春泥造物首页
      path: '/pottery',
      name: 'pottery',
      component: PotteryIndex
    },
    {
      // 购物车页面
      path: '/pottery/shopping_car',
      name: 'shopping_car',
      component: ShoppingCar
    }




  ],
});




