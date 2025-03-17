import React from 'react';
import { connect, history } from 'umi';
import { Alert, Button, Form, Input, Radio, Modal, Divider } from "antd";
import { LockOutlined, LoginOutlined, UserOutlined } from '@ant-design/icons';
import styles from './index.less';
import RegisteredModal from './registeredModal';
/**
 * 登录组件，负责用户登录和注册功能的展示与处理。
 */
class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      modalVisible: false // 控制注册模态框的可见性
    }
  }

  /**
   * 提交表单时的处理函数，发送登录请求。
   * @param {Object} value 表单值，包含用户名和密码。
   */
  onSubmit = async value => {
    const payload = {
      username: value.username,
      password: value.password
    };
    await this.props.dispatch({type: 'loginModel/login', payload: payload});
    if (this.props.isLogin === true) {
      Modal.success({
        centered: true,
        title: `${this.props.username}，欢迎回来`,
        content: `您的账户类型是${this.props.user_role}，点击确定即可进入用户首页.`,
        onOk: () => {
          this.linkToPage()
        }
      });
    }
  };

  /**
   * 处理退出登录操作。
   */
  logoutBtn = async () => {
    await this.props.dispatch({type: 'loginModel/logout'});
  };

  /**
   * 判断用户是否是管理员或普通用户，并跳转到相应页面。
   */
  linkToPage = () => {
    if (this.props.user_role === "user") history.push("/questionBank");
    else if (this.props.user_role === "admin") history.push("/admin");
  };

  /**
   * 打开注册模态框。
   */
  modalVisible = async () => {
    await this.setState({ modalVisible: true })
  };

  /**
   * 关闭注册模态框。
   */
  modalHide = async () => {
    await this.setState({ modalVisible: false })
  };

  /**
   * 初始化数据，用于加载登录状态。
   */
  initData = async () => {
    await this.props.dispatch({type: 'loginModel/getLoginStatus'})
  };

  /**
   * 组件将要挂载时，调用初始化数据函数。
   */
  componentWillMount() {
    this.initData().then(()=>null)
  }

  render() {
    /**
     * 根据登录状态渲染不同的提示信息。
     * @returns {JSX.Element} 登录状态提示。
     */
    const renderLoginTip = () => {
      if (this.props.isLogin === true) {
        return (
            <div>
              <Alert message={
                <div style={{fontSize: '0.8em'}}>
                  <div style={{margin: '0 0 5px 0'}}>{this.props.username + "已登陆，用户类型是：" + this.props.user_role}</div>
                  <div>
                    您可以：
                    <span className={styles.logout_btn} onClick={this.linkToPage}>进入首页</span>
                    ，或：
                    <span className={styles.logout_btn} onClick={this.logoutBtn}>注销登陆</span>
                  </div>
                </div>
              }
                     type="success"
                     className={styles.login_status_tip}
              />
              <Divider />
            </div>
        )
      } else {
        return <div className={styles.login_status_tip}></div>
      }
    };

    /**
     * 渲染登录表单。
     * @returns {JSX.Element} 登录表单。
     */
    const renderLoginForm = () => {
      return (
          <Form
              name="normal_login"
              className={styles.login_form}
              onFinish={this.onSubmit}
          >
            <Form.Item
                name="username"
                rules={[
                  {
                    required: true,
                    message: '请在此输入你的账号',
                  },
                ]}
            >
              <Input prefix={<UserOutlined className="site-form-item-icon"/>} placeholder="账号"/>
            </Form.Item>
            <Form.Item
                name="password"
                rules={[
                  {
                    required: true,
                    message: '请在此输入你的密码',
                  },
                ]}
            >
              <Input prefix={<LockOutlined className="site-form-item-icon"/>} type="password" placeholder="密码"/>
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" className={styles.login_form_button} icon={<LoginOutlined/>} loading={this.state.isLoading}>登录</Button>
              <Button type="link" onClick={this.modalVisible}>注册账号</Button>
            </Form.Item>
          </Form>
      )
    };
    return (
        <div className={styles.login_container}>
          <div className={styles.login_card}>
            <span className={styles.welcome_text}>登录</span>
            {renderLoginTip()}
            {renderLoginForm()}
          </div>
          <RegisteredModal visible={this.state.modalVisible}
                           hide={this.modalHide}
                           dispatch={this.props.dispatch}
          />
        </div>
    );


  }
}

/**
 * 从store中映射登录状态到组件的props。
 * @param {Object} state 应用的状态。
 * @returns {Object} 映射后的props。
 */
function mapStateToProps({ loginModel }) {
  const { isLogin, username, user_role } = loginModel;
  return { isLogin, username, user_role };
}

/**
 * 使用connect将组件连接到Redux store。
 * @param {Object} state 登录状态。
 * @returns {Object} 连接后的组件。
 */
export default connect(mapStateToProps)(Login);
