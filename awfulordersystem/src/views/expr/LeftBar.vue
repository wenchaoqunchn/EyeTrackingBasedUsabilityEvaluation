<template>
  <div id="invisible-border">
    <img src="../../assets/北京工业大学logo字.png" class="initImg fillImg" />
  </div>

  <el-menu
      default-active="1"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      router
  >
<!--    <el-menu-item index="1" route="/expr/MyHome/News" class="My Home">-->
    <el-menu-item index="1" @click="HomeClick" class="My Home">
      <i class="el-icon-menu"></i>
      <template #title>
        <span v-if="proxy.$Accessibility">Моя домашняя страница</span>
        <span v-else>My Home</span>
      </template>
    </el-menu-item>
<!--    <el-menu-item index="2" route="/expr/MyLearning/Library" class="My Learning">-->
    <el-menu-item index="2" @click="LearningClick" class="My Learning">
      <i class="el-icon-setting"></i>
      <template #title>
        <span v-if="proxy.$Accessibility">Мое обучение</span>
        <span v-else>My Learning</span>
      </template>
    </el-menu-item>
  </el-menu>
</template>

<script>
import { getCurrentInstance } from 'vue'
export default {
  setup() {
    const { proxy } = getCurrentInstance();
    return {
      proxy
    }
  },
  name: "LeftBar",
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    HomeClick() {
      this.$router.push("/expr/MyHome/News");
    },
    LearningClick() {
      this.$router.push("/expr/MyLearning/Library");
    }
  },
}
</script>

<style>
.initImg {
  width: 100%;
}
.fillImg {
  object-fit: contain;
}
#invisible-border {
  padding: 10px;
}
</style>