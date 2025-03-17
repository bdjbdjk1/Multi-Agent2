import React from 'react';
import { connect, history } from 'umi';
import { Layout, Menu, Button } from 'antd';
import {
  HomeOutlined,
  MehOutlined,
  OrderedListOutlined,
  EditOutlined,
  FileAddOutlined,
  HistoryOutlined,
  UserOutlined,
  LoginOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined
} from '@ant-design/icons';

const { Sider, Content, Header } = Layout;

class SideMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
    };
  }

  componentDidMount() {
    this.props.dispatch({ type: 'loginModel/getLoginStatus' });
  }

  toggle = () => {
    this.setState({ collapsed: !this.state.collapsed });
  };

  render() {
    const onClick = e => {
      if (history.location.pathname !== e.key) history.push(e.key);
    };

    const menu = () => {
      if (history.location.pathname === "/login" || history.location.pathname === "/home") {
        return null;
      } else if (history.location.pathname === "/admin") {
        const items = [
          {
            key: "/admin",
            icon: <HomeOutlined />,
            label: "管理员首页"
          },
          {
            key: "/login",
            icon: <LoginOutlined />,
            label: "退出"
          }
        ];
        return (
            <Menu items={items} mode="inline" theme='dark' onClick={onClick} selectedKeys={[history.location.pathname]} />
        );
      } else {
        const items = [
          {
            key: "/home",
            icon: <HomeOutlined />,
            label: "首页"
          },
          {
            key: "/agent",
            icon: <MehOutlined />,
            label: "智能体"
          },
          {
            key: "/questionBank",
            icon: <OrderedListOutlined />,
            label: "试题库显示"
          },
          {
            key: "/questionEdit",
            icon: <EditOutlined />,
            label: "添加或修改"
          },
          {
            key: "/questionGenerator",
            icon: <FileAddOutlined />,
            label: "组卷功能"
          },
          {
            key: "/questionGenHistory",
            icon: <HistoryOutlined />,
            label: "出题历史"
          },
          {
            key: "/login",
            icon: <UserOutlined />,
            label: `退出登陆：${this.props.username}`
          }
        ];
        return (
            <Menu items={items} mode="inline" theme='dark' onClick={onClick} selectedKeys={[history.location.pathname]} />
        );
      }
    };

    const isSidebarVisible = !(history.location.pathname === "/login" || history.location.pathname === "/home");

    return (
        <Layout style={{ minHeight: '100vh' }}>
          {isSidebarVisible && (
              <Sider collapsible collapsed={this.state.collapsed} onCollapse={this.toggle}>
                {menu()}
              </Sider>
          )}
          <Layout>
            {isSidebarVisible && (
                <Header style={{ background: '#fff', padding: 0 }}>
                  <Button type="primary" onClick={this.toggle} style={{ marginBottom: 16 }}>
                    {React.createElement(this.state.collapsed ? MenuUnfoldOutlined : MenuFoldOutlined)}
                  </Button>
                </Header>
            )}
            <Content style={{ margin: '16px' }}>
              {this.props.children}
            </Content>
          </Layout>
        </Layout>
    );
  }
}

function mapStateToProps({ loginModel }) {
  const { username } = loginModel;
  return { username };
}

export default connect(mapStateToProps)(SideMenu);