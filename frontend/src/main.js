
import Antd from 'ant-design-vue';
import { createApp } from 'vue';
import App from './App.vue'; // 确保引入的是 .vue 文件
import router from './router'; // 引入 router
import 'ant-design-vue/dist/reset.css'; // 引入 Ant Design 样式

// 创建 Vue 应用实例
const app = createApp(App);

// 使用 router 插件
app.use(router);
app.use(Antd); 
// 挂载到 #app
app.mount('#app');