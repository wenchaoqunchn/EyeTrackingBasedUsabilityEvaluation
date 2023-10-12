<template>
  <el-row>
<!--    选择日期-->
    <el-col :span="16">
      <el-calendar v-model="value" />
    </el-col>

<!--    选择开始时间-->
    <el-col :span="4">
      <table align="center">
        Select start time:
        <tr v-for="time in times1" :key="time">
          <td style="padding-top: 10px; padding-bottom: 10px" v-bind:id="'begin-'+time"  @click="link('begin-'+time)">
            {{time}}
          </td>
        </tr>
      </table>
    </el-col>

<!--    选择结束时间-->
    <el-col :span="4">
      <table align="center">
        Select end time:
        <tr v-for="time in times2" :key="time">
          <td style="padding-top: 10px; padding-bottom: 10px" v-bind:id="'end-'+time" @click="link('end-'+time)">
            {{time}}
          </td>
        </tr>
      </table>
    </el-col>
  </el-row>
  <center>
    <br>
    <el-button type="primary" @click="$router.push('/expr/MyLearning/Booking/SelectSpace')">Before</el-button>
    <el-button type="primary" @click="$router.push('/expr/MyLearning/Booking/Confirm')">Next</el-button>
  </center>
</template>

<script>
import { ref } from 'vue'
const value = ref(new Date())
export default {
  name: "SelectDate",
  data() {
    return {
      value,
      times1 : [
          "08:00",
          "09:00",
          "10:00",
          "11:00",
          "12:00",
          "13:00",
          "14:00",
          "15:00",
          "16:00",
          "17:00",
          "18:00",
      ],
      times2 : [
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
      ]
    }
  },
  methods: {
    link(id) {
      // console.log(id)
      // if id begin with "begin"
      if (id.substring(0, 5) == "begin") {
        for (let time in this.times1){
          document.getElementById("begin-"+this.times1[time]).style.backgroundColor = "";
        }
        let stop = id.substring(6, id.length)
        let visited = stop != "08:00" ? false : true
        for (let time in this.times2){
          // console.log(this.times2[time], stop, this.times2[time] == stop)
          if (this.times2[time] == stop) {
            document.getElementById("end-"+this.times2[time]).style.pointerEvents = "none";
            document.getElementById("end-"+this.times2[time]).style.color = "#ccc";
            visited = true
          }
          else {
            if (visited) {
              document.getElementById("end-"+this.times2[time]).style.pointerEvents = "all";
              document.getElementById("end-"+this.times2[time]).style.color = "#000";
            }
            else {
              document.getElementById("end-"+this.times2[time]).style.pointerEvents = "none";
              document.getElementById("end-"+this.times2[time]).style.color = "#ccc";
            }
          }
        }

        for (let time in this.times2){
          document.getElementById("end-"+this.times2[time]).style.backgroundColor = "";
        }
      }
      else {
        for (let time in this.times2){
          document.getElementById("end-"+this.times2[time]).style.backgroundColor = "";
        }
      }
      document.getElementById(id).style.backgroundColor = "#696969";
    }
  }
}
</script>

<style>
td:hover {
  background: gray;
}
.seat {
  padding: 10px 20px;
}
</style>