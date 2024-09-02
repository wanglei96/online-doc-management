<template>
    <div style="margin-left: 10px;">
        <a-space style="width: 100%; text-align: right">
                <a-button v-if = "is_superuser" type="primary" @click="showModal" style="margin-left: 10px;" >添加标签</a-button>    
            </a-space>
            <a-modal v-model:open="tag_open" title="添加标签" ok-text="添加" cancel-text="取消"  @ok="add_tag">
                  <a-form
                  :model="tag_info"
                  name="basic"
                  :label-col="{ span: 3 }"
                  :wrapper-col="{ span: 0 }"
                  autocomplete="off"
                >
                  <a-form-item
                    label="标签名"
                    name="tag_name"
                    :rules="[{ required: true, message: '请输入标签名!' }]"
                  >
                    <a-input  v-model:value="tag_info.tag_name" />
                  </a-form-item>
                  <a-form-item
                    label="标签序号"
                    name="sort_order"
                    @Input="onInput"
                    type="number"
                  >
                     <a-input  v-model:value="tag_info.sort_order" />
                  </a-form-item>
             
                    </a-form>
              </a-modal>

            <a-table :columns="columns" :data-source="data">
            <template #headerCell="{ column }">
                <template v-if="column.key === 'tag_name'">
                    <span>
                        <smile-outlined />
                        标签名
                    </span>
                </template>
            </template>

            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'order'">
                    <a>
                        {{ record.sort_order }}
                    </a>
                </template>

                <template v-else-if="column.key === 'action'">
                    <span>
                        <a-popconfirm
                            title="是否确定删除？"
                            ok-text="是"
                            cancel-text="否"
                            @confirm="del_file_tag(record.id)"
             
                          >
                            <a v-if = "is_superuser" href="#" >删除</a>
                          </a-popconfirm>
                        <a-divider type="vertical" />
                        <a @click="handleEdit(record)" v-if = "is_superuser">修改</a>
     
                    </span>
                </template>
            </template>
        </a-table>
        <a-modal v-model:open="edit_tag_open" title="修改标签" ok-text="修改" cancel-text="取消"  @ok="edit_tag">
                          <a-form
                          :model="edit_tag_info"
                          name="basic"
                          :label-col="{ span: 3 }"
                          :wrapper-col="{ span: 0 }"
                          autocomplete="off"
                        >
                          <a-form-item
                            label="标签名"
                            name="new_tag_name"
                            :rules="[{ required: true, message: '请输入标签名!' }]"
                          >
                            <a-input  v-model:value="edit_tag_info.new_tag_name" />
                          </a-form-item>
                          <a-form-item
                            label="标签序号"
                            name="new_sort_order"
                            @Input="edit_onInput"
                            type="number"
                          >
                             <a-input  v-model:value="edit_tag_info.new_sort_order" />
                          </a-form-item>
             
                            </a-form>
                      </a-modal>
    </div>
</template> 

<script setup>
import {get_file_tags, get_current_user_role , delete_file_tag ,
     add_file_tag, edit_file_tag } from '@/api';
import { ref, onMounted, computed , reactive } from 'vue';
import { message } from 'ant-design-vue';


const columns = [
    {
        name: '标签名',
        dataIndex: 'tag_name',
        key: 'tag_name',
    },
    {
        title: '排序',
        key: 'order',
        dataIndex: 'order',
    },
    {
        title: '操作',
        key: 'action',
    },
];
const data = ref([]);


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

const get_tags = async () => {
    try {
        const response = await get_file_tags();
        data.value = response.data;
    } catch (error) {
        console.error(error);
    }
}

const del_file_tag  = async (id) => {   
    try {
        const response = await delete_file_tag(id);
        message.success('删除成功');
        console.info(response)
        location.reload();
    } catch (error) {
        message.error('删除失败');
        console.error(error);
    }
}

const tag_open = ref(false);
const showModal = () => {
    tag_open.value = true;
};

const tag_info = reactive({
    tag_name: ref(""),
    sort_order: ref(0),
})

const add_tag = async () => {   
    try {
        tag_info.sort_order = parseInt(tag_info.sort_order);
        const response = await add_file_tag(tag_info);
        message.success('添加成功');
        console.info(response)
        get_tags();
        tag_open.value = false;
        location.reload();
    } catch (error) {
        message.error('添加失败');
        console.error(error);
    }
}

const  onInput = (event) => {
    const value = event.target.value;
    if (!/^\d*$/.test(value)) {
        event.target.value = value.replace(/\D/g, '');  // 移除非数字字符
    }
    if (parseInt(event.target.value) < 0) {
        event.target.value = 0;  // 确保值不小于0
    }
    tag_info.sort_order = event.target.value;
}

const edit_tag_info = reactive({
    id: ref(0),
    new_tag_name: ref(""),
    new_sort_order: ref(0),
})

const edit_tag_open = ref(false);

const handleEdit = (item) => {
    edit_tag_open.value = true;
    edit_tag_info.id = item.id
    edit_tag_info.new_tag_name = item.tag_name
    edit_tag_info.new_sort_order = item.sort_order   
}

const edit_tag = async () => {   
    try {
        edit_tag_info.new_sort_order = parseInt(edit_tag_info.new_sort_order);
        console.log(edit_tag_info)
        const response = await edit_file_tag(edit_tag_info);
        message.success('修改成功');
        console.info(response)
        get_tags();
        edit_tag_open.value = false;
        location.reload();
    } catch (error) {
        message.error('修改失败');
        console.error(error);
    }
}

const edit_onInput = (event) => {
    const value = event.target.value;
    if (!/^\d*$/.test(value)) {
        event.target.value = value.replace(/\D/g, '');  // 移除非数字字符
    }
    if (parseInt(event.target.value) < 0) {
        event.target.value = 0;  // 确保值不小于0
    }
    edit_tag_info.new_sort_order = event.target.value;
}

onMounted(() => {   
    get_tags();
    getrole();  
});

</script>