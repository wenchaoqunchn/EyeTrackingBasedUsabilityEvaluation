<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    router
  >
    <!--    <el-menu-item index="1" route="/expr/MyHome/News">News</el-menu-item>-->
    <el-menu-item index="1" @click="NewsClick">
      <span v-if="proxy.$Accessibility">Новости</span>
      <span v-else>News</span>
    </el-menu-item>
    <!--    <el-menu-item index="2" route="/expr/MyHome/Agenda">Agenda</el-menu-item>-->
    <el-menu-item index="2" @click="AgendaClick">
      <span v-if="proxy.$Accessibility">Повестка дня</span>
      <span v-else>Agenda</span>
    </el-menu-item>
    <!--    <el-menu-item index="3" route="/expr/MyHome/More">More</el-menu-item>-->
    <el-menu-item index="3" @click="MoreClick">
      <span v-if="proxy.$Accessibility">Подробнее</span>
      <span v-else>More</span>
    </el-menu-item>
  </el-menu>
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
  name: "MyHomeHeadBar",
  data() {
    return {
      activeIndex: "1",
    };
  },
  methods: {
    NewsClick() {
      this.$router.push("/expr/MyHome/News");
    },
    AgendaClick() {
      this.$router.push("/expr/MyHome/Agenda");
    },
    MoreClick() {
      this.$router.push("/expr/MyHome/More");
    },
  },
};
</script>

<style scoped></style>
