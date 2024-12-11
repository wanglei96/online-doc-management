<template>
  <a-layout>
    <a-layout-header style="background: #fff; padding: 0; display: flex; justify-content: space-between; align-items: center;">
      <router-view name="header" />
      <a-space style="margin-left: auto; padding-right: 20px;">
        <a-button @click="logout">退出</a-button>
      </a-space>
    </a-layout-header>
  </a-layout>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
    name: "AppHeader",
    setup() {
        const router = useRouter();

        const logout = () => {
            localStorage.setItem('token', '');
            router.push({ path: '/' });
        };

        return {
            logout
        };
    }
};
</script>

<style scoped>
/* 你可以根据需要调整样式 */
</style>
