<template>
  <div id="screen-center">
    <el-button type="primary"  id="verLarge" @click="handleClick">
<!--      <router-link to="/expr/MyHome/News">Ready > </router-link> -->
      Ready >
    </el-button>
    BadDesigns
    <br>
    Accessibility: {{proxy.$Accessibility}}
    <br>
    Ease_of_use: {{proxy.$Ease_of_use}}
    <br>
    Accuracy: {{proxy.$Accuracy}}
    <br>
    Consistency: {{proxy.$Consistency}}
    <br>
    Device_efficiency: {{proxy.$Device_efficiency}}
    <br>
    Robustness: {{proxy.$Robustness}}
  </div>
</template>

<script>
import axios from "axios";
import { getCurrentInstance } from 'vue'

export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy
    }
  },
  name: "Ready",
  methods: {
    handleClick() {
      axios.post('/api/start_record', {
        unix_timestamp : Math.floor(Date.now()),
        Accessibility : this.proxy.$Accessibility,
        Ease_of_use : this.proxy.$Ease_of_use,
        Accuracy : this.proxy.$Accuracy,
        Consistency : this.proxy.$Consistency,
        Device_efficiency : this.proxy.$Device_efficiency,
        Robustness : this.proxy.$Robustness
      }).then(response => {
        console.log(response)
      })
      this.$router.push("/expr/MyHome/News");
    }
  },
}
</script>

<style scoped>
#screen-center {
  text-align: center; /*让div内部文字居中*/
  background-color: #fff;
  border-radius: 20px;
  width: 300px;
  height: 350px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

#verLarge {
  font-size: 50px;
  font-weight: bold;
  margin-top: 20px;
  padding: 50px;
}
</style>