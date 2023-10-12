<template>
  <center>
    <h1>Select the venue you want to visit</h1>
  </center>
  <el-row>
    <el-col
        :span="6"
        :offset="0"
    >
      <el-card :body-style="{ padding: '0px' }" shadow="hover" @click="handleClick('1')">
        <img
            src="../../../../assets/北馆.jpg"
            class="image"
        />
        <div style="padding: 14px" id="1">
          <span><h1>North Library</h1></span>    <el-tag size="small">open</el-tag>
          <br>
          The North Library was built in 1960 and put into use in 1982, covering an area of more than 8,000 square meters; in 1992, the library automated its operations with self-developed library management software, becoming one of the first libraries in China to realize computer management; in 1997, the library established an electronic reading room and began to provide CD-ROM database search, multimedia CD-ROM reading and Internet access In 1997, the library established an electronic reading room and started to provide CD-ROM database search, multimedia CD-ROM reading and Internet access.
          <br>
<!--          <el-radio v-model="radio1" label="1" size="large">预定</el-radio>-->
        </div>
      </el-card>
    </el-col>
    <el-col
        :span="6"
        :offset="2"
    >
      <el-card :body-style="{ padding: '0px' }" shadow="hover" @click="handleClick('2')">
        <img
            src="../../../../assets/南馆.jpg"
            class="image"
        />
        <div style="padding: 14px" id="2">
          <span><h1>South Library</h1></span>    <el-tag size="small">open</el-tag>
          <br>
          The South Library was built and put into use in 2002, covering an area of 12,000 square meters. By the end of 2013, the library has more than 1.3 million volumes of paper books in Chinese and foreign languages, more than 1200 kinds of periodicals and magazines in Chinese and foreign languages, and more than 70 domestic and foreign network literature databases. It has formed a literature resource system based on paper-based resources and multiple carriers such as paper, electronic and video, mainly in engineering, and in multiple disciplines such as science, engineering, administration and literature, which meets most of the information needs of teaching and research of the university.<br>
<!--          <el-radio v-model="radio1" label="2" size="large">预定</el-radio>-->
        </div>
      </el-card>
    </el-col>
    <el-col
        :span="6"
        :offset="2"
    >
      <el-card :body-style="{ padding: '0px' }" shadow="hover" @click="handleClick('3')">
        <img
            src="../../../../assets/逸夫图书馆.jpg"
            class="image"
        />
        <div style="padding: 14px" id="3">
          <span><h1>Yifu Library</h1></span>    <el-tag size="small">open</el-tag>
          <br>
          The Yifu Library is converted and expanded from the South Library and will be completed in 2019. The total construction area of the renovated and expanded Yifu Library of BIT is 40,463 square meters, of which the old library area is reserved at 4,570 square meters, the new area is 28,938 square meters, and the underground area is 6,955 square meters. The building height is 23.9 meters with five floors above ground and one floor underground. The building covers an area of 12539㎡, and the volume ratio and building density are balanced for the whole campus because it is located on the campus. The entire library has a collection of 2,512,000 books.<br>
<!--          <el-radio v-model="radio1" label="3" size="large">预定</el-radio>-->
        </div>
      </el-card>
    </el-col>
  </el-row>

  <center>
    <br>
    <el-button type="primary" @click="handleNextClick">Next</el-button>
  </center>
</template>

<script>
import { ref } from 'vue'
import { getCurrentInstance } from 'vue'

const radio1 = ref('1')
export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy
    }
  },
  name: "SelectSpace",
  data () {
    return {
      radio1,
    }
  },
  methods : {
    handleNextClick () {
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
    handleClick(e) {
      for (let i = 1; i < 4; i++){
        document.getElementById(i).style.backgroundColor='';
      }
      if (this.proxy.$Accuracy){
        if (e == "1")
          e = "2"
        else if (e == "2")
          e = "3"
        else if (e == "3")
          e = "1"
      }
      let i = document.getElementById(e)
      // console.log(i)
      i.style.backgroundColor='gray';
    },
  }
}
</script>

<style>
.time {
  font-size: 12px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
</style>