<template>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0; display: flex; justify-content: space-between; align-items: center;">
        <router-view name="header" />
        <a-space>
          <a-button style="margin-left: 1130px" @click="logout">退出</a-button>
        </a-space>
      </a-layout-header>
    </a-layout>

</template>

<script>
import { useRouter } from 'vue-router';

export default {
    name: "AppHeader",
setup(){
            const router = useRouter()

            const logout = () =>{
                localStorage.setItem('token', '')
                router.push({path: '/'})
        }
        return {
            logout
        };

        }


};

</script>

<style scoped>
/* .logo {
    height: 32px;
    margin: 16px;
    background: rgba(245, 246, 246, 0.2);
} */
</style>