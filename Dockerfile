FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -i 'https://pypi.tuna.tsinghua.edu.cn/simple' -r requirements.txt
RUN pip3 install -i 'https://pypi.tuna.tsinghua.edu.cn/simple' uwsgi

COPY . .

CMD ["honcho", "start", "web"]
