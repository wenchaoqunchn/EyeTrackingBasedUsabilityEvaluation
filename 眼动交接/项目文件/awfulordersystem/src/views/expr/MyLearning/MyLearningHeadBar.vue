<template>
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      router
  >
<!--    <el-menu-item index="1" route="/expr/MyLearning/Library">Library</el-menu-item>-->
<!--    <el-menu-item index="2" route="/expr/MyLearning/Booking">Booking</el-menu-item>-->
<!--    <el-menu-item index="3" route="/expr/MyLearning/More">More</el-menu-item>-->
    <el-menu-item index="1" @click="LibraryClick">Library</el-menu-item>
    <el-menu-item index="2" @click="BookingClick">Booking</el-menu-item>
    <el-menu-item index="3" @click="MoreClick">More</el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: "MyLearningHeadBar",
  data() {
    return {
      activeIndex: "1",
    };
  },
  methods: {
    LibraryClick() {
      this.$router.push("/expr/MyLearning/Library");
    },
    BookingClick() {
      this.$router.push("/expr/MyLearning/Booking");
    },
    MoreClick() {
      this.$router.push("/expr/MyLearning/More");
    }
  }
}
</script>

<style scoped>

</style>