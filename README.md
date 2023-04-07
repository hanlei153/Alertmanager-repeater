# Alertmanager-repeater
#### Alertmanager-repeater是一个可以将prometheus告警转发至飞书、钉钉、企业微信的一个告警转发器，实现告警功能

### 克隆存储库

    git clone https://github.com/henlei153/Alertmanager-repeater.git
### 运行转发器，将$SERVER_PORT替换为你想监听的端口，-w用来指定worker进程的数量
    cd Alertmanager-repeater/bin
    gunicorn Alertmanager-repeater:server -w 6 -b 0.0.0.0:$SERVER_PORT

### 容器运行，容器默认运行在8080端口，如果需要修改请更改dockerfile中的ENV
    cd Alertmanager-repeater
    docker build -t image:tag .
    docker run -it --name container_name -p port:port image:tag
### Alertmanager配置文件中修改webhook配置
    "receivers":
    - "name": "prometheus-feishu-webhook"
      "webhook_configs":
      - "url": "http://IP:port/api/feishu"

### 钉钉、企业微信告警正在开发中...
