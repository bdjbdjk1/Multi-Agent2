import { defineConfig } from 'umi';

export default defineConfig({
  // 加速构建
  mfsu: {},
  // cdn目录
  publicPath: "/static/",


  // 国际化
  locale: {
    default: 'zh-CN',
    antd: true
  },
  history: {
    type: 'hash'
  },
  routes: [
    {
      path: '/',
      component: '@/layouts/index',
      routes: [

        // 登陆
        { path: '/login',  exact: true, component: '@/pages/login', title: "多智能体组卷系统" },
        { path: '/',  exact: true, redirect: '/home' },

        // 管理员
        {exact: true, path: '/admin', component: '@/pages/admin', title: "组卷系统-管理员"},

        // 用户
        {exact: true, path: '/home', component: '@/pages/home', title: "组卷系统-首页"},
        {exact: true, path: '/agent', component: '@/pages/agent', title: "组卷系统-智能体"},
        {exact: true, path: '/questionBank', component: '@/pages/questionBank', title: "组卷系统-题库"},
        {exact: true, path: '/questionEdit', component: '@/pages/questionEdit', title: "组卷系统-编辑"},
        {exact: true, path: '/questionGenerator', component: '@/pages/questionGenerator', title: "组卷系统-组卷"},
        {exact: true, path: '/questionGenHistory', component: '@/pages/questionGenHistory', title: "组卷系统-历史记录"},
        // {exact: true, path: '/questionManager', component: '@/pages/questionManager', title: "组卷系统"}
      ]
    }
  ],
  plugins: [],
  devServer:{
    port: 8081,
  }
});
