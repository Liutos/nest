# nest

管理用户、任务，以及计划等数据的服务端程序。

# 构建和启动

`nest`仓库中包含了构建 Docker 镜像所需的`Dockerfile`文件，直接运行如下命令即可

```shell
sudo docker build -t nest .
```

构建成功后，准备一份配置文件，内容如下

```ini
[mysql]
database = 数据库名称
host = MySQL 实例的主机名
password = 连接 MySQL 的帐号的密码
user = 连接 MySQL 的帐号的用户名

[redis]
db = Redis 中逻辑数据库的编号
host = Redis 实例的主机名
port = Redis 实例监听的端口号
```

假设将上述内容保存到文件`${confi_dir}/default.ini`中，那么启动容器的命令为

```shell
sudo docker run -d -i -p 9090:9090 -t -v "${config_dir}":/app/nest/web/config/ nest
```

启动成功后，可以用如下命令验证其正在监听宿主机的 9090 端口号

```shell
lsof -i:9090
```

# 运行单元测试

```shell
MODE=local_unittest pytest -ra -s -x ./
```

# 启动一个开发 fledgling 用的测试环境

运行下列命令

```shell
honcho start web
```

便可以在本地机器上启动 nest，监听 9090 端口。
