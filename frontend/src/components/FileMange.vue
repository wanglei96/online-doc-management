<template>

    <div>
      <a-space style="width: 95%; text-align: right">
       <a-button v-if = "is_superuser" type="primary" style="width: 100px"  @click="showModal" >上传文件</a-button> 
      </a-space>
      
      <a-modal v-model:open="open" title="上传文件" ok-text="上传" cancel-text="取消"  @ok="handleUp">
        <div class="down">
        <a-upload-dragger
          class="up_word"
          :fileList="fileList"
          name="file"
          :max-count="1"
          :multiple="false"
          accept=".pdf"
          method="post"
          :before-upload="beforeUpload"
          @change="handleChange"
          @remove="handleRemove"
        >
          <div class="up-text">
            <p class="ant-upload-drag-icon">
              <inbox-outlined></inbox-outlined>
            </p>
            <p class="ant-upload-text">点击上传文件</p>
            <p class="ant-upload-hint">支持(.pdf)</p>
          </div>
          
        </a-upload-dragger>
        <a-form
              :model="file_tag"
              name="basic"
              :label-col="{ span: 5 }"
              :wrapper-col="{ span: 0 }"
              autocomplete="off"
            >
        <a-form-item
                  label="文件标签"
                  name="tag"
                  :rules="[{ required: true, message: '请输入文件标签!' }]"
                >
          <a-input v-model:value="file_tag.tag" />
        </a-form-item>
        </a-form>
        <!-- <div class="r_b">
          <a-button type="dashed" style="margin-right: 50px">取消</a-button>
          <a-button type="primary" @click="handleUp">提交</a-button>
        </div> -->
      </div>

      </a-modal>
    </div>
     <a-divider />

  <div>
    <!-- 文件列表 -->
    <a-list item-layout="horizontal" :data-source="data" >
      <template #renderItem="{ item }">

        <a-list-item>
          <a-list-item-meta>
            <template #title>
              <a class="left-aligned">{{ item.filename }}</a>
            </template>
            <template #avatar>
              <a-avatar src="/wendang.png" />
            </template>
            <!-- <template #description>
              <a class="left-aligned">{{ item.file_tag }}</a>
            </template> -->
          </a-list-item-meta>
          <template #actions>
                <a key="list-loadmore-edit" :href="'/web/viewer.html?file=' + handlefilepath(item.filename)"
                >预览</a>
                <a @click="handlefileopen(item)" v-if = "is_superuser">修改</a>
                <a-popconfirm
                    title="是否确定删除？"
                    ok-text="是"
                    cancel-text="否"
                    @confirm="deletefile(item.id)"
             
                  >
                    <a href="#" v-if = "is_superuser">删除</a>
                  </a-popconfirm>
                <!-- <a key="list-loadmore-more" @click="deletefile(item.id)">删除</a> -->
              </template>
              <div>{{item.file_tag}}</div>
        </a-list-item>
      </template>
    </a-list>
    <a-modal v-model:open="file_open" title="修改文件信息" ok-text="修改" cancel-text="取消"  @ok="edit_file_info">
              <a-form
              :model="file_info"
              name="basic"
            
              :label-col="{ span: 3 }"
              :wrapper-col="{ span: 0 }"
              autocomplete="off"
            >
              <a-form-item
                label="文件名"
                name="filename"
                :rules="[{ required: true, message: '请输入文件名!' }]"
              >
                <a-input  v-model:value="file_info.filename" />
              </a-form-item>
              <a-form-item
                label="标签"
                name="file_tag"
                :rules="[{ required: true, message: '请输入文件标签!' }]"
              >
                <a-input v-model:value="file_info.file_tag" />
              </a-form-item>
             
                </a-form>
          </a-modal>
  </div>
  <!-- <a-modal v-model:open="open_file" title="预览" cancel-text="关闭" width="800px" height="500px">
  <iframe id="pdfViewer" width="600" height="400"></iframe>
  </a-modal> -->
</template>


<script setup>
import { listFiles, uploadfile , delete_file , get_current_user_role , edit_file } from '@/api';
import { ref, onMounted, computed, reactive , watch } from 'vue';
import { message } from 'ant-design-vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const data = ref([]);
const fileType = ref(route.query.fileType || '');

const handlefilepath = (filename) => {
  
  return process.env.VUE_APP_API_BASE_URL + '/files/' + filename
}


const getfiles = async () => {
  try {
    console.log(fileType.value)
    console.log('fileType.value:'+fileType.value);
    const response = await listFiles(fileType.value);
    file_info.file_tag = fileType.value;
    data.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

const deletefile = async (id) => {

  try {
    const response = await delete_file(id);
    message.success('删除成功');
    console.info(response)
    getfiles();
  } catch (error) {
    console.error(error);
  }
};


onMounted(() => {
  getfiles();
  getrole();
});

watch(() => route.query.fileType, (newFileType) => {
  fileType.value = newFileType || '';
  getfiles();
}, { immediate: true });

const open = ref(false);
const showModal = () => {
  open.value = true;
};
// const handleOk = e => {
//   console.log(e);
// open.value = false;
// };


// 上传文件的限制
const fileList = ref([]);
const handleRemove = (file) => {
  const index = fileList.value.indexOf(file);
  const newFileList = fileList.value.slice();
  newFileList.splice(index, 1);
  fileList.value = newFileList;
};

const beforeUpload = (file) => {
  fileList.value = [...(fileList.value || []), file];
  return false;
};

const handleChange = (info) => {
  if (fileList.value.length === 2) {
    const newFileList = fileList.value.slice();
    newFileList.splice(0, 1);
    fileList.value = newFileList;
  }
  console.log(fileList.value.length);
  // 文件上传状态的控制
  const status = info.file.status;
  if (status !== "uploading") {
    console.log(info.file, info.fileList);
  }
  if (status === "done") {
    message.success(`${info.file.name} file uploaded successfully.`);
  } else if (status === "error") {
    message.error(`${info.file.name} file upload failed.`);
  }
};

const file_tag = reactive({
  tag: ref("")
});

// 调用上传字典的接口
const handleUp = async () => {
  try {
    // 组件含有的方法，获取文件的相关信息
    const formData = new FormData(); //创建的对象，用于封装要上传的文件和其他需要传递的数据
    formData.append("file", fileList.value[0]);
    formData.append("file_tag", file_tag.tag);
    
    console.log(formData);
    console.log(fileList.value[0]);
    // console.log(localStorage.getItem('token'));
    const response = await uploadfile(localStorage.getItem('token'), formData);
    console.log(response);
    open.value = false;
    getfiles();
    location.reload();
  } catch (error) {
    console.error(error);
    message.error("上传失败！");
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

const file_info = reactive({
  id: ref(0),
  filename: ref(""),
  file_tag: ref(""),
})

const file_open = ref(false)

const handlefileopen = (item) => {
  file_open.value = true;
  file_info.id = item.id;
  file_info.filename = item.filename;
  file_info.file_tag = item.file_tag;
}

const edit_file_info = async () => {
  try {
    const response = await edit_file(file_info);
    console.log(response);
    file_open.value = false;
    getfiles();
    message.success('修改成功');
    location.reload();
  } catch (error) {
    message.error('修改失败');
    console.error(error);
  }
}

</script>

<style scoped>
.left-aligned {
  text-align: left; /* 确保文本左对齐 */
  display: block;   /* 确保文本占据整行 */
}
.ppt-preview {
  margin-top: 20px;
  height: 600px;
  /* 调整为你需要的高度 */
  
}
</style>