<template>
  <div id="container"></div>
</template>

<script>
  // 在这个组件内监听三个值，分别是父组件传过来的过去七天的日期列表和代码统计列表，以及num表示当前接收了几个值
  // 当date_counte或者date_list接收到父组件传来的值时，num就加1，同时监听num，当num>=2时说明两个数都已经接收到，就触发生成图表的函数
  import Highcharts from 'highcharts'
  export default {
        name: "charts",
        data(){
          return {
            num: 0,
          }
        },
        props: ["date_counts", "date_list"],
        watch:{
          date_counts: function(new_data, old_data){
            this.num += 1;
          },
          date_list: function(new_data, old_data){
            this.num += 1;
          },
          num: function(new_data, old_data){
            if(new_data >= 2){
              this.generate_chart()
            }
          }
        },
        methods:{
          generate_chart(){
                      Highcharts.chart('container', {
            chart: {
              type: 'line'
            },
            title: {
              text: '最近七天代码行数图'
            },
            subtitle: {
              text: '数据来源: 数据库'
            },
            xAxis: {
              categories: this.date_list
            },
            yAxis: {
              title: {
                text: '代码行数 (行)'
              }
            },
            plotOptions: {
              line: {
                dataLabels: {
                  // 开启数据标签
                  enabled: true
                },
                // 关闭鼠标跟踪，对应的提示框、点击事件会失效
                enableMouseTracking: false
              }
            },
            series: [{
              name: '当前用户',
              data: this.date_counts
            }, ]
          })
          }
        },
    }

</script>

<style scoped>
#container{
  min-width:00px;
  height:400px;
  margin-top: 70px;
}
</style>
