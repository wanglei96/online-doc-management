<template>
    <div style="margin-left: 10px;" >
        <a-space style="width: 100%; text-align: right">
            <a-button v-if = "is_superuser" type="primary" @click="showModal" style="margin-left: 10px;" >添加用户</a-button>    
        </a-space>
        
        <a-divider />
        <a-modal v-model:open="open" title="添加用户" ok-text="添加" cancel-text="取消"  @ok="register">
            <a-form
                :model="register_info"
                name="basic"
                :rules="rules"
                :label-col="{ span: 3 }"
                :wrapper-col="{ span: 21 }"
                autocomplete="off"
                ref="formRef"
                >
                <a-form-item label="用户名" name="username">
                    <a-input v-model:value="register_info.username" />
                </a-form-item>
                <a-form-item label="密码" name="password">
                    <a-input-password v-model:value="register_info.password" />
                </a-form-item>
                <a-form-item label="角色" name="is_admin">
                    <a-select
                    v-model:value="register_info.is_admin"
                    :options="options"
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
                        <a v-if = "is_superuser" href="#" >删除</a>
                      </a-popconfirm>
                    <a-divider type="vertical" />
                            <a-modal v-model:open="edit_open" title="编辑用户" ok-text="提交" cancel-text="取消"  @ok="editUser">
                            <a-form
                            :model="editperson_info"
                            name="basic"
                            :rules="rules"
                            :label-col="{ span: 3 }"
                            :wrapper-col="{ span: 21 }"
                            autocomplete="off"
                            ref="formRef"
                        >
                            <a-form-item
                            label="用户名"
                            name="username"
                            >
                            <a-input  v-model:value="editperson_info.username" />
                            </a-form-item>
                            <a-form-item
                            label="新密码"
                            name="password"
                            >
                            <a-input-password  v-model:value="editperson_info.password" />
                            </a-form-item>

                            <a-form-item
                                label="角色"
                                name="is_admin"
                            >
                                <a-select
                                v-model:value="editperson_info.is_admin"
                                style="width: 100%"
                                :options="options"
                            ></a-select>
                            </a-form-item>
                            
                            </a-form>
        </a-modal>
                    <a @click="handleeditUser(record)" v-if = "is_superuser">修改</a>
                </span>
            </template>
        </template>
    </a-table>
</template>
<script setup>
import { user_info , register_user , delete_personal , get_current_user_role, edit_user } from '@/api';
import { ref, onMounted , reactive, computed } from 'vue';
import { message } from 'ant-design-vue';

const rules = {
  username: [{ required: true, message: "请输入用户名！", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码！", trigger: "blur" }],
  is_admin: [{ required: true, message: "请配置角色！", trigger: "blur" }],
};


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


const register_info = reactive({
    "username": ref(""),
    "password": ref(""),
    "is_admin": ref(),
    
});

const handleeditUser = (record) => {
    editperson_info.id = record.id
    editperson_info.username = record.username
    editperson_info.is_admin = record.is_admin
    edit_open.value = true
}


const editperson_info = reactive({
    "id": ref(0), 
    "username": ref(""),
    "password": ref(""),
    "is_admin": ref(0),
    
});

const resetForm = (form) => {
  for (const key in form) {
    form[key] = typeof form[key] === "object" ? ref("") : null;
  }
};

const reset_register_info = () => resetForm(register_info);
const reset_editperson_info = () => resetForm(editperson_info);

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

// 表单引用
const formRef = ref(null);

const register =async () => {
    try {
        // 调用表单校验
        await formRef.value.validate();
        const response = await register_user(register_info);
        message.success('添加成功');
        console.info(response)
        open.value = false;
        getpersonal();
    } catch (error) {
        console.error(error);
    }
};

const editUser = async () => {
    try {
// 调用表单校验
        await formRef.value.validate();
        const response = await edit_user(editperson_info);
        message.success('修改成功');
        console.info(response)
        edit_open.value = false;
        editperson_info.password = ref("");
        getpersonal();
    } catch (error) {
        console.error(error);
    }
};


const open = ref(false);
const edit_open = ref(false);

const showModal = () => {
    open.value = true;
};

const getpersonal = async () => {
    reset_register_info()
    reset_editperson_info()
    try {
        const response = await user_info();
        console.log(response.data);
        data.value = response.data;
    } catch (error) {
        console.error(error);
    }
};

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
    getpersonal();
    getrole();
});
// export { };
</script>