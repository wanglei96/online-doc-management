<template>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <router-view name="header" />
        <a-space style="width: 100%; text-align: right">

            <a-button style="margin-left: 8px" @click="logout">退出</a-button>
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