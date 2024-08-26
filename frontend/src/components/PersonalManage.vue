<template>
    <div style="margin-left: 10px;" >
        <a-space style="width: 100%; text-align: right">
            <a-button type="primary" @click="showModal" style="margin-left: 10px;" >添加用户</a-button>    
        </a-space>
        
        <a-divider />
        <a-modal v-model:open="open" title="添加用户" ok-text="添加" cancel-text="取消"  @ok="register">
            <a-form
            :model="register_info"
            name="basic"
            
            :label-col="{ span: 3 }"
            :wrapper-col="{ span: 0 }"
            autocomplete="off"
            @finish="handleSubmit"
          >
            <a-form-item
              label="用户名"
              name="username"
              :rules="[{ required: true, message: '请输入用户名!' }]"
            >
              <a-input  v-model:value="register_info.username" />
            </a-form-item>
            <a-form-item
              label="密码"
              name="password"
              :rules="[{ required: true, message: '请输入密码!' }]"
            >
              <a-input-password  v-model:value="register_info.password" />
            </a-form-item>

            <a-form-item
                label="角色"
                name="is_admin"
                :rules="[{ required: true, message: '请配置角色!' }]"
            >
                <a-select
                v-model:value="value"
                style="width: 100%"
                :options="options"
                @change="handleChange"
                
            ></a-select>
            </a-form-item>
             
              </a-form>
        </a-modal>
    </div>
    
    <a-table :columns="columns" :data-source="data">
        <template #headerCell="{ column }">
            <template v-if="column.key === 'name'">
                <span>
                    <smile-outlined />
                    Name
                </span>
            </template>
        </template>

        <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'name'">
                <a>
                    {{ record.name }}
                </a>
            </template>

        <template v-else-if="column.key === 'is_admin'">
            <span>
                {{ record.is_admin === 1 ? '管理员' : '普通用户' }}
            </span>
        </template>

            <template v-else-if="column.key === 'action'">
                <span>
                    <a-popconfirm
                        title="是否确定删除？"
                        ok-text="是"
                        cancel-text="否"
                        @confirm="handleDelete(record.id)"
             
                      >
                        <a href="#" >删除</a>
                      </a-popconfirm>
                    <a-divider type="vertical" />
     
                </span>
            </template>
        </template>
    </a-table>
</template>
<script setup>
import { user_info , register_user , delete_personal } from '@/api';
import { ref, onMounted , reactive} from 'vue';
import { message } from 'ant-design-vue';

const columns = [
    {
        name: 'Name',
        dataIndex: 'username',
        key: 'username',
    },
    {
        title: '角色',
        key: 'is_admin',
        dataIndex: 'is_admin',
    },
    {
        title: '操作',
        key: 'action',
    },
];
const data = ref([]);

const options = ref([
    {
        value: 0,
        label: '普通用户',
    },
    {
        value: 1,
        label: '管理员',
    },
]);
const value = reactive([]);
const handleChange = value => {
    register_info.is_admin = value;
    console.log(`selected ${value}`);
};

const register_info = reactive({
    "username": ref(""),
    "password": ref(""),
    "is_admin": ref(),
    
});

const reset_register_info = () =>{
   register_info.username = null
   register_info.password = null
   register_info.is_admin = ref()
   value.values = null
}


// const del_info = {
//     'id': ref(),
//     'is_admin': ref(),
// }

const handleDelete = async (id) => {
    try {
        // console.log(data);
        // const user_id = data[id]
        console.log(id);
        // console.log(localStorage.getItem('token'));
        const response = await delete_personal(id);
        message.info(response.data.message);
        console.info(response)
        getpersonal();
    } catch (error) {
        console.error(error);
    }
};

const register =async () => {
    try {
        const response = await register_user(register_info);
        message.success('添加成功');
        console.info(response)
        open.value = false;
        getpersonal();
    } catch (error) {
        console.error(error);
    }
};

const handleSubmit =() => {
    open.value = false;
        getpersonal();
}



const open = ref(false);
const showModal = () => {
    open.value = true;
};

const getpersonal = async () => {
    reset_register_info()
    try {
        const response = await user_info();
        console.log(response.data);
        data.value = response.data;
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    getpersonal();
    // reset_register_info();
});
// export { };
</script>