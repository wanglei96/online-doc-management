<template>
    <a-form
        :model="formState"
        name="basic"

        :label-col="{ span: 10 }"
        :wrapper-col="{ span: 5 }"
        autocomplete="off"
        @finish="handleSubmit"
      >
        <a-form-item
          label="Username"
          name="username"
          :rules="[{ required: true, message: '请输入用户名!' }]"
        >
          <a-input v-model:value="formState.username" />
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :rules="[{ required: true, message: '请输入密码!' }]"
        >
          <a-input-password v-model:value="formState.password" />
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 10, span: 5 }">
          <a-button type="primary" html-type="submit">登录</a-button>
        </a-form-item>
      </a-form>
</template>

<script>
import { defineComponent, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
// import axios from 'axios';
import { login } from '@/api';


export default defineComponent({
    setup() {
        const router = useRouter();
        const formState = reactive({
            username: '',
            password: '',
        });
        // const response = {
        //     access_token: '',
        // };

        const rules = {
            username: [{ required: true, message: 'Please input your username' }],
            password: [{ required: true, message: 'Please input your password' }]
        };

        const handleSubmit = async () => {
            try {
                // console.log(formState);
                const resp = await login(formState.username, formState.password);
                localStorage.setItem('token', resp.data.access_token);
                // console.log('***********');
                // console.log(resp.data.access_token);
                // console.log('#########');
                // console.log(localStorage.getItem('token'));
                message.success('Login successful');
                router.push('/FileMange'); // 登录成功后跳转到仪表盘页面
            } catch (error) {
                console.error('Login failed:', error);
                message.error('Invalid username or password');
            }
        };

        

        return {
            formState,
            rules,
            handleSubmit
        };
    }
});
</script>

<style scoped>
a-card {
    width: 100%;
}
</style>
