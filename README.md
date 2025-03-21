# 在线组卷系统

## 介绍
![Alt text](https://raw.githubusercontent.com/bdjbdjk1/Multi-Agent2/refs/heads/master/photo.jpg)

技术栈：后端 Java SpringBoot + 前端 React 


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
mvn spring-boot:run
```

前端：标准webpack工程，在package.json目录下执行npm install拉取依赖，npm start运行工程，npm build构建工程。

```shell
npm install
npm run build
npm start
```

数据库：记得导入数据库表结构，默认utf8mb4，数据库表结构sql文件已包含建库、建表语句。

```shell
mysql -u root -h host -p < xxx.sql
```
