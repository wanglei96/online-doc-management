<template>
  <a-layout style="min-height: 100vh " >
    <!-- 侧边栏 -->
    <AppSidebar v-if="showSidebar" />

    <!-- 主内容 -->
    <a-layout>
      <!-- <a-layout-header style="background: #fff; padding: 0">
        <router-view name="header" />
      </a-layout-header> -->
      <a-layout-content style="margin: 24px 16px 0">
        <div style="padding: 24px; background: #fff; min-height: 600px">
          <router-view />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import AppSidebar from "@/components/AppSidebar.vue";

export default {
  name: "App",
  components: {
    AppSidebar,
  },
  computed: {
    showSidebar() {
      return this.$route.path !== '/login' && this.$route.path !== '/';
    },
  },
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

