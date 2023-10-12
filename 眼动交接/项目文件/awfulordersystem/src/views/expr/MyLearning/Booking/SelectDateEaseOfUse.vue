<template>
  <el-row>
<!--    选择日期-->
    <el-col :span="16">
      <el-calendar v-model="value" />
    </el-col>

<!--    选择开始时间-->
    <el-col :span="4">
      <table align="center">
        <tr v-for="time in times1" :key="time">
          <td style="padding-top: 10px; padding-bottom: 10px" v-bind:id="'begin-'+time"  @click="link($event, 'begin-'+time)">
            {{time}}
          </td>
        </tr>
      </table>
    </el-col>

<!--    选择结束时间-->
    <el-col :span="4">
      <table align="center">
        <tr v-for="time in times2" :key="time">
          <td style="padding-top: 10px; padding-bottom: 10px" v-bind:id="'end-'+time" @click="link($event, 'end-'+time)">
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
    link(e, id) {
      // console.log(e.clientX, e.clientY, this.getPosition(document.getElementById(id)))
      let postion = this.getPosition(document.getElementById(id))
      // console.log("click in position:", (e.clientX > postion["x_min"] && e.clientX < postion["x_max"]) &&  (e.clientY > postion["y_min"] && e.clientY < postion["y_max"]))
      if (!(e.clientX > postion["x_min"] && e.clientX < postion["x_max"] &&  e.clientY > postion["y_min"] && e.clientY < postion["y_max"])) {
        return
      }
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
    },
    getElementLeft(element){
  var actualLeft = element.offsetLeft;
  var current = element.offsetParent;

  while (current !== null){
    actualLeft += current.offsetLeft;
    current = current.offsetParent;
  }

  return actualLeft;
},
    getElementTop(element){
  var actualTop = element.offsetTop;
  var current = element.offsetParent;

  while (current !== null){
    actualTop += current.offsetTop;
    current = current.offsetParent;
  }

  return actualTop;
},
    getPosition(element) {
      let left = this.getElementLeft(element)
      let top = this.getElementTop(element)
      // console.log("width:", element.offsetWidth, "height:", element.offsetHeight)
      let padding = 18
      return {"x_min": left+padding, "y_min": top+padding, "x_max": left + element.offsetWidth-padding, "y_max": top + element.offsetHeight-padding}
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