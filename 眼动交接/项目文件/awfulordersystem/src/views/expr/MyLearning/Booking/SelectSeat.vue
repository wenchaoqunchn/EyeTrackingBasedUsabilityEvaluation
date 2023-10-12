<template>

  <table align="center">
    <tr v-for="row in rows" :key="row">
      <td v-for="id in row" align="center" :key="id" @click="link(id)">
        <div class="seat" v-bind:id="id">
          <img width="50" src="../../../../assets/sofa-removebg-preview-small.png">
          <br>
          {{ id }}
        </div>
      </td>
    </tr>
  </table>



  <center>
    <br>
    <el-button type="primary" @click="handleBeforeClick">Before</el-button>
    <el-button type="success" @click="finish" >Submit</el-button>
  </center>
</template>

<script>
import { getCurrentInstance } from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import router from "@/router";

export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy
    }
  },
  name: "SelectSeat",
  data () {
    return {
      select : "",
      rows : [
        [
          "101",
          "102",
          "103",
          "104",
          "105",
          "106",
          "107",
          "108",
          "109",
          "110",
        ],
        [
          "201",
          "202",
          "203",
          "204",
          "205",
          "206",
          "207",
          "208",
          "209",
          "210",
        ],
          [
          "301",
          "302",
          "303",
          "304",
          "305",
          "306",
          "307",
          "308",
          "309",
          "310",
          ],
          [
          "401",
          "402",
          "403",
          "404",
          "405",
          "406",
          "407",
          "408",
          "409",
          "410",
          ]
      ]
    }
  },
  methods: {
    handleBeforeClick () {
      if (this.proxy.$Consistency){
        this.$router.push('/expr/MyLearning/Booking/SelectDateConsistency')
      }
      else if (this.proxy.$Ease_of_use){
        this.$router.push('/expr/MyLearning/Booking/SelectDateEaseOfUse')
      }
      else {
        this.$router.push('/expr/MyLearning/Booking/SelectDate')
      }
    },
    finish() {
      // this.$message({
      //   message: "finish",
      //   type: "success"
      // });
      if (this.select == "") {
        ElMessageBox.alert("Please select a seat", "Error");
      } else {
        ElMessageBox.alert('您已成功预定一个座位,id:'+this.select, '预定成功', {
          confirmButtonText: 'OK',
        }).then(() => {
          ElMessage({
            type: 'success',
            message: '即将退出',
          })
          // window.close();
          // window.open("about:blank","_self").close()
          router.push("/leave");
        })
      }

    },
    link(id) {
      // console.log(e.target.innerText);
      // alert(e.currentTarget.innerHTML );
      // alert(id);
      // console.log(this.rows);
      for(let row in this.rows) {
        // console.log(row);
        for(let seat in this.rows[row]) {
          document.getElementById(this.rows[row][seat]).style.backgroundColor = "";
          // console.log(this.rows[row][seat]);
        }
      }
      document.getElementById(id).style.backgroundColor = "#696969";
      this.select = id;
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