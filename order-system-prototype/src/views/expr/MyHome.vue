<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <MyHomeHeadBar />
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import MyHomeHeadBar from "./MyHome/MyHomeHeadBar.vue";
export default {
  name: "MyHome",
  components: {
    MyHomeHeadBar,
  },
};
</script>

<style></style>
