<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <MyLearningHeadBar/>
      </el-header>

      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import MyLearningHeadBar from "@/views/expr/MyLearning/MyLearningHeadBar";
export default {
  name: "MyLearning",
  components: {
    MyLearningHeadBar
  }
}
</script>

<style>
:deep(.zero-padding) {
  padding: 0;
}
</style>