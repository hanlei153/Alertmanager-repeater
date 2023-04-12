FROM python:3.9-alpine3.17
MAINTAINER HANLEI
WORKDIR /opt
COPY . /opt/Alertmanager-repeater
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
	cd /opt/Alertmanager-repeater && pip3 install gunicorn && pip3 install -r requirements.txt
ENV WORKER=4 SERVER_PORT=8080
CMD ["sh", "-c", "cd /opt/Alertmanager-repeater/bin && gunicorn Alertmanager-repeater:server -w $WORKER -b 0.0.0.0:$SERVER_PORT"]
