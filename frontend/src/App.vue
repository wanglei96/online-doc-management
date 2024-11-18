<template>
  <a-layout style="min-height: 100vh " >
    <!-- 侧边栏 -->
    <AppSidebar v-if="showComponents" />

    <!-- 主内容 -->
    <a-layout>
      <AppHeader v-if="showComponents" />
      <a-layout-content >
        <div style="padding: 0px; background: #fff; min-height: 600px">
          <router-view />
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import AppSidebar from "@/components/AppSidebar.vue";
import AppHeader from "@/components/AppHeader.vue";


export default {
  name: "App",
  components: {
    AppSidebar,
    AppHeader
  },
  
  computed: {
    showComponents() {
      return this.$route.path !== '/';
    },
  
}
}


</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  /* margin-top: 60px; */
}
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

