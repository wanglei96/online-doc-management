<template>

    <div>
      <a-space style="width: 95%; text-align: right">
       <a-button type="primary" style="width: 100px"  @click="showModal" >上传文件</a-button> 
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
          <a-list-item-meta >
            <template #title>
              <a class="left-aligned">{{ item.filename }}</a>
            </template>
            <template #avatar>
              <a-avatar src="/wendang.png" />
            </template>
          </a-list-item-meta>
          <template #actions>
                <a key="list-loadmore-edit" :href="'/web/viewer.html?file=' + handlefilepath(item.filename)"
                >预览</a>
                <a-popconfirm
                    title="是否确定删除？"
                    ok-text="是"
                    cancel-text="否"
                    @confirm="deletefile(item.id)"
             
                  >
                    <a href="#" >删除</a>
                  </a-popconfirm>
                <!-- <a key="list-loadmore-more" @click="deletefile(item.id)">删除</a> -->
              </template>
        </a-list-item>
      </template>
    </a-list>
  </div>
</template>


<script setup>
import { listFiles, uploadfile , delete_file } from '@/api';
import { ref, onMounted} from 'vue';
import { message } from 'ant-design-vue';
// import * as pdfjsLib from 'pdfjs-dist';

const data = ref([]);

const handlefilepath = (filename) => {
  return process.env.VUE_APP_API_BASE_URL + '/files/' + filename
}


const getfiles = async () => {
  try {
    const response = await listFiles();
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
});



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

// 调用上传字典的接口
const handleUp = async () => {
  try {
    // 组件含有的方法，获取文件的相关信息
    const formData = new FormData(); //创建的对象，用于封装要上传的文件和其他需要传递的数据
    formData.append("file", fileList.value[0]);

    console.log(fileList.value[0]);
    // console.log(localStorage.getItem('token'));
    const response = await uploadfile(localStorage.getItem('token'), formData);
    console.log(response);
    open.value = false;
    getfiles();
  } catch (error) {
    console.error(error);
    message.error("上传失败！");
  }
};

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