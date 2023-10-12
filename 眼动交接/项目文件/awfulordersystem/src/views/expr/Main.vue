<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px"><LeftBar/></el-aside>
        <el-main><router-view/></el-main>
    </el-container>
  </div>
</template>

<script>
import LeftBar from "@/views/expr/LeftBar";
export default {
  name: "Main",
  components: {
    LeftBar,
  },
};
</script>
