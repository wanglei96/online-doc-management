<template>

  <div class="login-page">
    <div class="login-container" >
      <div class="title">用户登录</div>
      <a-form
        :model="formState"
        name="basic"
        autocomplete="off"
        @finish="handleSubmit"
      >
        <a-form-item
          label="用户名"
          name="username"
          :rules="[{ required: true, message: '请输入用户名!' }]"
        >
          <a-input v-model:value="formState.username" placeholder="请输入用户名" />
        </a-form-item>

        <a-form-item
          label="密码"
          name="password"
          style="margin-left: 15px;"
          :rules="[{ required: true, message: '请输入密码!' }]"
        >
          <a-input-password v-model:value="formState.password" placeholder="请输入密码" />
        </a-form-item>

        <a-form-item>
          <a-button type="primary" html-type="submit" style="width: 35%; height: auto;" block>登录</a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>

</template>

<script>
import { defineComponent, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import { login } from '@/api';

export default defineComponent({
  setup() {
    const router = useRouter();
    const formState = reactive({
      username: '',
      password: '',
    });

    const handleSubmit = async () => {
      try {
        const resp = await login(formState.username, formState.password);
        localStorage.setItem('token', resp.data.access_token);
        message.success('登录成功');
        router.push('/FileMange'); // 登录成功后跳转
      } catch (error) {
        console.error('登录失败:', error);
        message.error('用户名或密码错误');
      }
    };

    return {
      formState,
      handleSubmit,
    };
  },
});
</script>

<style>
/* 页面整体样式 */
body 
html {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: auto; /* 禁止滚动条 */
  font-family: 'Roboto', sans-serif;
}

/* 登录页面背景样式 */
.login-page {
  height: 100vh; /* 确保填满视口高度 */
  width: 100vw; /* 确保填满视口宽度 */
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f3f358, #2575fc, #34e89e); /* 渐变背景 */
  background-size: cover; /* 确保背景填满 */
  background-position: center; /* 居中背景 */
}

/* 登录框样式 */
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 30px 40px;
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 20px; /* 圆角边框 */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25); /* 阴影 */
  text-align: center;
}

/* 标题样式 */
.title {
  font-size: 25px;
  font-weight: bold;
  color: #333;
  margin-bottom: 25px;
}

/* 表单项对齐样式 */
a-form-item {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: space-between;
  margin-bottom: 20px;
}

/* 标签样式 */
a-form-item label {
  flex: 0 0 60px; /* 固定标签宽度 */
  text-align: right;
  color: #333;
  font-weight: bold;
  margin-right: 10px;
}

/* 输入框样式 */
a-input,
a-input-password {
  flex: 1; /* 输入框占据剩余空间 */
  border-radius: 10px;
  padding: 8px 12px;
  background-color: rgba(245, 245, 245, 1);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

a-input:hover,
a-input-password:hover {
  border-color: #40a9ff;
  box-shadow: 0 0 6px rgba(64, 169, 255, 0.3); /* 悬停效果 */
}

/* 登录按钮样式 */
a-button {
  background: linear-gradient(135deg, #34e89e, #2575fc);
  color: white;
  font-weight: bold;
  border: none;
  height: 45px;
  border-radius: 10px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.16);
  transition: all 0.3s ease;
  width: 0%;
  margin-top: 10px;
}

a-button:hover {
  transform: scale(1.05);
  background: linear-gradient(135deg, #2575fc, #34e89e);
}

/* 占位符颜色 */
input::placeholder {
  color: #aaa;
}
</style>



