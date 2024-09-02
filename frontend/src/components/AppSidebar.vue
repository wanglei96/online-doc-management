<template>

    <a-layout-sider collapsible theme="dark" :trigger="null"
        :style="{ overflow: 'auto', height: '100vh', position: 'relative', left: 0, top: 0, bottom: 0 }">
        <div class="logo"/>
        <a-menu
            v-model:openKeys="openKeys"
            v-model:selectedKeys="selectedKeys"
            style="width: 256px; overflow: auto;"
            theme="dark"
            mode="inline"
            :items="items"
            @click="handleClick"
        >
        </a-menu>
    </a-layout-sider>
</template>

<script>
import { get_current_user_role , get_file_tags } from '@/api';
import { reactive, ref, h , computed, onMounted ,onBeforeMount } from 'vue';
import { FilePdfOutlined, TeamOutlined ,TagOutlined,SettingOutlined } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';

export default {
    name: "AppSidebar",

setup() {
        // const key = ref(0);
        const router = useRouter();
        const selectedKeys = ref(['1']);
        const openKeys = ref(['sub1']);
        function getItem(label, key, icon, children, type) {
            return {
                label,
                key,
                icon,
                children,
                type,
            };
        }

        const tags = reactive([]);
        const get_tags = async () => {
            try {
                const role_resp = await getrole()
                const response = await get_file_tags();
                // console.log("Response Data:", response.data);
                // console.log("Data Type:", Array.isArray(response.data)); // 应该返回 true
                tags.splice(0, tags.length, ...response.data.map(item => item.tag_name));
                if (Array.isArray(response.data)) {
                    tags.unshift('全部');
                    const newItems = tags.map(tag => getItem(tag, tag, () => h(TagOutlined)));
                    // console.log(items);
                    // console.log(newItems);
                    items[0].children = newItems; // 更新菜单项的子菜单
                } else {
                    console.error("Response data is not an array.");
                }
                console.log(":"+role_resp);
                if (role_resp !== 1) {
                    console.log("role_resp:"+role_resp); 
                    console.log(items)
                    const indexToRemove = items.findIndex(item => item.label === '人员管理' || item.label === '配置中心');

                    // 如果找到索引，则使用 splice 方法移除项
                    if (indexToRemove !== -1) {
                        items.splice(indexToRemove, 2);
                    }
                    console.log("items::::"+items)
                }
            } catch (error) {
                console.error(error);
            }
        };
        

        const items = reactive(
            [
            getItem('文件管理', 'filemanage', () => h(FilePdfOutlined), []),
            getItem('人员管理', 'personmanage', () => h(TeamOutlined)),
            getItem('配置中心', 'configcenter', () => h(SettingOutlined), [getItem('文件标签配置', 'tagconfig', () => h(SettingOutlined))]
        ),
        ]
    );
        const handleClick = (e) => {
            console.log('click', e);
            const key = e.key; // 获取点击的菜单项 key
            if (tags.includes(key))  {
                router.push({ path: '/FileMange',  query: { fileType: key } });
                console.log('key:'+key);
            }
            switch (key) {
                case 'personmanage':
                    router.push('/PersonalManage');
                    break;
                case 'tagconfig':
                    router.push('/FileTagsConfig');
                    break;
                default:
                    break;
            }
        };

    const role = ref('');

    const getrole= async() => {
    try {
        const response = await get_current_user_role();
        role.value = response.data.role;
        // message.info(response.data.message);
        console.info(role)
        return role.value
    } catch (error) {
        console.error(error);
    }
}

const is_superuser = computed(() => {
    return role.value !== 0
})

// watch(is_superuser, (newValue) => {
//     if (!newValue) {
//         // 如果 is_superuser 为 false，删除数组中的某个值
//         console.log(11111111);
//         items.concat = items.filter(item => item.key !== 'personmanage');
//         console.log(items.concat);
//         key.value += 1
//     }
// });
onBeforeMount(() => {
    getrole();
})

onMounted(() => {
    get_tags()
});
// onBeforeMount(
//     () => {
//         // getrole();
//         get_tags();
//     }
// )
return {
    is_superuser,
    selectedKeys,
    openKeys,
    items,
    handleClick,
}


}


};





</script>

<style scoped>
.logo {
    height: 42px;
    margin: 18px;
    margin-bottom: 20px;
    /* background: rgb(238, 204, 79); */
    background-image: url('/public/logo.PNG'); /* 设置背景图片 */
    background-size: cover; /* 使图片覆盖整个div */
    background-position: center; /* 图片居中显示 */
    background-repeat: no-repeat; /* 防止图片重复 */
}
.ant-menu-item {
  text-align: left; /* 确保文本左对齐 */
}
</style>
