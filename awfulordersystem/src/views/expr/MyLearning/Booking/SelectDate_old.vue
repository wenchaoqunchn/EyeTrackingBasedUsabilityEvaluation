<template>
  <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">选择日期</span>
      <el-date-picker
          v-model="value1"
          type="date"
          placeholder="Pick a day"
          :disabled-date="disabledDate"
          @click="onClick(a)"
      />
    </div>
    <div class="block">
      <span class="demonstration">选择开始时间</span>
      <el-time-select
          v-model="value"
          start="08:30"
          step="00:30"
          end="18:30"
          placeholder="Select time"
          @click="onClick(b)"
      />
    </div>
    <div class="block">
      <span class="demonstration">选择结束时间</span>
      <el-time-select
          v-model="value2"
          start="09:00"
          step="00:30"
          end="19:00"
          placeholder="Select time"
          @click="onClick(c)"
      />
    </div>
  </div>
  <center>
    <br>
    <el-button type="primary" @click="$router.push('/expr/MyLearning/Booking/SelectSpace')">Before</el-button>
    <el-button type="primary" @click="$router.push('/expr/MyLearning/Booking/SelectSeat')">Next</el-button>
  </center>
</template>

<script>
import { ref } from 'vue'
const value1 = ref('')
const value2 = ref('')
const value = ref('')
export default {
  name: "SelectDate",
  data () {
    return {
      value1,
      value,
      value2,
      elementsPosition : {},
    }
  },
  methods: {
    disabledDate (date) {
      return date && date.valueOf() < Date.now() - 86400000
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
    scanChildNode(node, path){
      node.setAttribute("data-path", path)
      let left = this.getElementLeft(node)
      let top = this.getElementTop(node)
      this.elementsPosition[path] = {"x1": left, "y1": top, "x2": left + node.offsetWidth, "y2": top + node.offsetHeight}

      let childNodes = node.childNodes;
      for(let i = 0; i < childNodes.length; i++){
        let childPath = path + (path === "" ? "" : ",") + i
        if (childNodes[i].nodeType === 1)
          this.scanChildNode(childNodes[i], childPath)
      }
    },

    async onClick(e) {
      console.log(e)
      // document.getElementsByClassName("el-popper")[1].style.left
    },
  }
}
</script>

<style scoped>
.demo-date-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}
.demo-date-picker .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.demo-date-picker .block:last-child {
  border-right: none;
}
.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>