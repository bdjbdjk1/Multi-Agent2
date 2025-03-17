# 在线组卷系统

## 介绍
![image]([https://github.com/cainiaoyige01/tingyu-cloud/blob/main/static/img/2.png](https://github.com/bdjbdjk1/Multi-Agent2/blob/master/%E5%9B%9B%E4%B8%AA%E6%A8%A1%E5%9D%97%E6%9E%B6%E6%9E%84%E5%9B%BE.jpg
)))

简介：自动组卷系统，遗传算法、贪心算法，支持导入题库，手动选择、自动组卷，生成排版美观的Word文档，前后端分离WebApp，Java SpringBoot + React

技术栈：后端 Java SpringBoot + 前端 React Umi.js

类型：WebApp

## 安装

### 目录结构

TestPapaerGen-Backend：后端

TestPapaerGen-Frontend：前端

数据库表结构：数据库

assets：示例文件

### 如何运行

后端：标准Java Maven SpringBoot工程，在pom.xml目录下执行mvn install拉取依赖后，mvn package打包jar包，推荐在idea环境下配置maven项目。

```shell
mvn install
mvn package
java -jar ./target/xxx.jar
```

前端：标准webpack工程，在package.json目录下执行npm install拉取依赖，npm start运行工程，npm build构建工程。

```shell
npm install
npm start
npm build
```

数据库：记得导入数据库表结构，默认utf8mb4，数据库表结构sql文件已包含建库、建表语句。

```shell
mysql -u root -h host -p < xxx.sql
```
