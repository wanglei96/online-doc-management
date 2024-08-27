// src/api.js
import axios from 'axios';

// Create an axios instance with a default configuration
const api = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL,  // Base URL from environment variable
    timeout: 1000,  // Optional: Set request timeout
});

// 添加请求拦截器
api.interceptors.request.use(config => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('token');
    if (token) {
        config.headers['Authorization'] = 'Bearer ' + token;
        // config.headers['Content-Type'] = 'application/json';
    }
    return config;
}, error => {
    // 对请求错误做些什么
    return Promise.reject(error);
});

// Define API methods
export const login = (username, password) => {
    // console.log(username, password);
    return api.post('/token', { grant_type: 'password', username, password, scope: 'scope', client_id : 'client_id', client_secret: 'client_secret' },
        {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }
)};

export const listFiles = (tag) => {
    // console.log('11111111111');
    if (!tag || tag === '全部') {
        return api.get('/files/');
    }
    return api.get('/files/', {params: {
        file_tag: tag
    }
    });
};

export const uploadfile = (token, formData) => {
    // console.log('11111111111');
    return api.post('/upload/', formData,
        {
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'multipart/form-data'
            }
        }
    );
};


export const user_info = () => {
    return api.get('/users/');
}

// Add more API methods as needed


export const register_user = (user_info) => {
    return api.post('/register/', user_info);
}


export const delete_personal = (user_id) => {
    const body = { id: user_id, }
    console.log(body);
    return api.delete('/delete_user/',
        {
            headers: {
                'Content-Type': 'application/json'
            },
        data: body
        }
    );
};


export const delete_file = (file_id) => {
    const body = { id: file_id, }
    console.log(body);
    return api.delete('/delete_file/',
        {
            headers: {
                'Content-Type': 'application/json'
            },
        data: body
        }
    );
};

export const get_pdf_base64 = (file_name) => {
    return api.get('/get_pdf_base64/', { file_name: file_name });
}

export const get_current_user_role = () => {
    return api.get('/current_user_role/');
}

export const edit_file = (file_info) => {
    return api.post('/edit_file/', file_info);
}

export const get_file_tags = () => {
    return api.get('/all_file_tags/');
}