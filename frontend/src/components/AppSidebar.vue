<template>
    <a-layout-sider collapsible theme="dark" style="background-color: #0e293c;" 
     :style="{ overflow: 'auto', height: '100vh', position: 'relative', left: 20, top: 0, bottom: 0 } ">
        <div class="logo"/>
        <a-menu theme="dark"  default-selected-keys="['1']" mode="inline" style="background-color: #12354e;">
            <a-menu-item key="1">
                <a-icon type=file />
                <span>文件列表</span>
                <router-link to="/FileMange"></router-link>
            </a-menu-item>
            <a-menu-item key="2" v-if = "is_superuser">
                    <a-icon type=person />
                    <span>人员管理</span>
                    <router-link to="/PersonalManage"></router-link>
                </a-menu-item>
            <!-- 其他导航项可以在这里添加 -->
        </a-menu>
    </a-layout-sider>
</template>

<script>
import { get_current_user_role } from '@/api';
import { ref, computed, onMounted } from 'vue';

export default {
    name: "AppSidebar",
setup() {
    const role = ref('');

    const getrole = async () => {
    try {
        const response = await get_current_user_role();
        role.value = response.data.role;
        // message.info(response.data.message);
        console.info(role)
    } catch (error) {
        console.error(error);
    }
}

const is_superuser = computed(() => {
    return role.value !== 0
})
onMounted(() => {
    getrole();
});

return {
    is_superuser
}



}


};





</script>

<style scoped>
.logo {
    height: 32px;
    margin: 16px;
    background: rgba(201, 223, 244, 0.853);
    background-image: url('/public/logo.PNG'); /* 设置背景图片 */
    background-size: cover; /* 使图片覆盖整个div */
    background-position: center; /* 图片居中显示 */
    background-repeat: no-repeat; /* 防止图片重复 */
}
</style>
