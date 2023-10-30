<template>
  <center v-loading="loading">
    <h1>
      Confirmation of venue and time of submission?<br />After searching, we
      will show you the available seats later
    </h1>

    <br />
    <el-button type="primary" @click="handleBeforeClick">Before</el-button>
    <el-button type="primary" @click="handleNextClick">Next</el-button>
  </center>
</template>

<script>
import { getCurrentInstance } from "vue";
export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy,
    };
  },
  name: "Confirm",
  data() {
    return {
      loading: false,
    };
  },
  methods: {
    handleBeforeClick() {
      if (this.proxy.$Consistency) {
        this.$router.push("/expr/MyLearning/Booking/SelectDateConsistency");
      } else if (this.proxy.$Ease_of_use) {
        this.$router.push("/expr/MyLearning/Booking/SelectDateEaseOfUse");
      } else {
        this.$router.push("/expr/MyLearning/Booking/SelectDate");
      }
    },
    handleNextClick() {
      if (this.proxy.$Device_efficiency) {
        console.log("Device_efficiency");
        this.$router.push(
          "/expr/MyLearning/Booking/SelectSeatDeviceEfficiency"
        );
      } else if (this.proxy.$Robustness) {
        this.$router.push("/expr/MyLearning/Booking/SelectSeatRobustness");
      } else {
        console.log("non thing");
        this.$router.push("/expr/MyLearning/Booking/SelectSeat");
      }
    },
  },
};
</script>

<style scoped></style>
