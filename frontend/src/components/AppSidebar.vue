<template>
    <a-layout-sider collapsible theme="dark" style="background-color: #0e293c;" 
     :style="{ overflow: 'auto', height: '100vh', position: 'relative', left: 20, top: 0, bottom: 0 } ">
        <!-- <div class="logo" /> -->
        <a-menu theme="dark"  default-selected-keys="['1']" mode="inline" style="background-color: #12354e;">
            <a-menu-item key="1">
                <a-icon type=file />
                <span>文件列表</span>
                <router-link to="/FileMange"></router-link>
            </a-menu-item>
            <a-menu-item key="2">
                    <a-icon type=person />
                    <span>人员管理</span>
                    <router-link to="/PersonalManage"></router-link>
                </a-menu-item>
            <!-- 其他导航项可以在这里添加 -->
        </a-menu>
    </a-layout-sider>
</template>

<script>
export default {
    name: "AppSidebar",
};
</script>

<style scoped>
/* .logo {
    height: 32px;
    margin: 16px;
    background: rgba(245, 246, 246, 0.2);
} */
</style>
