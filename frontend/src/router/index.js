

import { getToken } from '@/utils/auth';
import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/components/LoginPage.vue';
import FileMange from '@/components/FileMange.vue';
import PersonalManage from '@/components/PersonalManage.vue';

const routes = [
    {
        path: '/',
        name: 'Login',
        component: Login
    },
    {
        path: '/FileMange',
        name: 'FileMange',
        component: FileMange,
        meta: { requiresAuth: true },
    },
    {
        path: '/PersonalManage',
        name: 'PersonalManage',
        component: PersonalManage,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    if (to.path !== '/login') {
        // 确保侧边栏在登录页面之外的所有页面中都显示
    }
    next();
});


router.beforeEach((to, from, next) => {
    const isAuthenticated = !!getToken();  // Replace with actual authentication check

    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
        next('/login');  // Redirect to login page if not authenticated
    } else {
        next();  // Proceed to the route
    }
});

export default router;
