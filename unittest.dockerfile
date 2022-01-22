FROM python:3.8

# 模仿 main.yml 中的操作。
RUN apt-get update -y
# 安装 MySQL 客户端，用于运行单元测试前自动建表。
RUN apt-get install -y default-mysql-client
# Set timezone
RUN ln -sf /usr/share/zoneinfo/Asia/ShangHai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -i 'https://pypi.tuna.tsinghua.edu.cn/simple' -r requirements.txt
RUN pip3 install -i 'https://pypi.tuna.tsinghua.edu.cn/simple' uwsgi

CMD ["bash", "run_unittest_in_docker_compose.sh"]
