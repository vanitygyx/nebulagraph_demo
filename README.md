# nebulagraph_demo
基于nebula-python客户端导入sqlite3数据进入nebula数据库中

# Nebula数据库部署

### 文件内容

```
config.py 保存了数据库所需的静态配置
load.py 主函数，创建库以及导入数据
new.py 保存创建TAG、EDGE的函数
utils.py 保存插入点、边的函数
```

### 前提

docker桌面版、git

### 使用docker安装（已启动docker服务）

1. 下载nebula数据库docker版

```bash
git clone -b release-3.4 https://github.com/vesoft-inc/nebula-docker-compose.git
cd nebula-docker-compose/
```

1. 启动nebula服务

```bash
[nebula-docker-compose]$ docker-compose up -d
```

1. 连接到数据库

```bash
#查看刚刚启动的docker容器名称
[nebula-docker-compose]$ docker-compose ps
#例子
Name                         Command             State                 Ports
--------------------------------------------------------------------------------------------
nebuladockercompose_console_1     sh -c sleep 3 &&          Up
                                  nebula-co ...
......
#进入容器

[nebula-docker-compose]$ docker exec -it nebula-docker-compose-console-1 /bin/sh
/ #

#连接nebula数据库（未设置时用户名默认为root）
/ # ./usr/local/bin/nebula-console -u root -p root --address=graphd --port=9669

#例子
Welcome!

(root@nebula) [(none)]>

#查看状态
(root@nebula) [(none)]> SHOW HOSTS
+-------------+------+----------+--------------+------------------------------------------------+------------------------------------------------+---------+
| Host        | Port | Status   | Leader count | Leader distribution                            | Partition distribution                         | Version |
+-------------+------+----------+--------------+------------------------------------------------+------------------------------------------------+---------+
| "storaged0" | 9779 | "ONLINE" | 5            | "demo_basketballplayer:3, demo_shareholding:2" | "demo_basketballplayer:3, demo_shareholding:2" | "3.4.0" |
| "storaged1" | 9779 | "ONLINE" | 4            | "demo_basketballplayer:3, demo_shareholding:1" | "demo_basketballplayer:3, demo_shareholding:1" | "3.4.0" |
| "storaged2" | 9779 | "ONLINE" | 6            | "demo_basketballplayer:4, demo_shareholding:2" | "demo_basketballplayer:4, demo_shareholding:2" | "3.4.0" |
+-------------+------+----------+--------------+------------------------------------------------+------------------------------------------------+---------+
Got 3 rows (time spent 2.244ms/3.881432ms)

Fri, 19 May 2023 05:35:32 UTC

#如果需要退出
(root@nebula) [(none)]> exit
```

1. 退出nebula停止服务

```bash
PS D:\label\nebula-docker-compose> docker-compose down
[+] Running 11/11
 ✔ Container nebula-docker-compose-console-1    Removed  10.4s                                                        
 ✔ Container nebula-docker-compose-graphd1-1    Removed  0.6s                                                          
 ✔ Container nebula-docker-compose-graphd2-1    Removed  0.8s                                                          
 ✔ Container nebula-docker-compose-graphd-1     Removed  0.6s                                                          
 ✔ Container nebula-docker-compose-storaged2-1  Removed  1.5s                                                          
 ✔ Container nebula-docker-compose-storaged0-1  Removed  1.2s                                                          
 ✔ Container nebula-docker-compose-storaged1-1  Removed  1.0s                                                          
 ✔ Container nebula-docker-compose-metad2-1     Removed  0.9s                                                          
 ✔ Container nebula-docker-compose-metad0-1     Removed  1.0s                                                          
 ✔ Container nebula-docker-compose-metad1-1     Removed  1.1s                                                          
 ✔ Network nebula-docker-compose_nebula-net     Removed  0.2s                                                          
```

### 可视化界面Nebula-Studio安装（docker版本）

1. 下载安装包

[](https://oss-cdn.nebula-graph.io/nebula-graph-studio/3.6.0/nebula-graph-studio-3.6.0.tar.gz)

1. 解压

```bash
mkdir nebula-graph-studio-3.6.0 -zxvf nebula-graph-studio-3.6.0.gz -C nebula-graph-studio-3.6.0

cd nebula-graph-studio-3.6.0
```

1. 运行容器

```bash
docker-compose pull
docker-compose up -d
```

4.浏览器连接

```bash
http://localhost:7001
```

![4dd5b9af17efd770d964b5e9b702ea4.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3207ca7e-4a9f-4f1d-b49e-6f96e7ec4f83/4dd5b9af17efd770d964b5e9b702ea4.png)

ipconfig查看ip地址并填入，用户名root，密码root

5.连接成功

![f34d8e5264004eafe8931ec6c15eeea.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2c13da44-ac9c-48d2-b80a-adc27df46781/f34d8e5264004eafe8931ec6c15eeea.png)
