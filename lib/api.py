import flask,json,os,configparser,requests
from lib.Time import utc_to_cst

server = flask.Flask(__name__)


#创建配置文件对象
con = configparser.ConfigParser()


#读取配置文件
config_path = config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'config.ini')
con.read(config_path, encoding='utf-8')

#获取所有section
sections = con.sections()



@server.route('/api/feishu', methods=['post'])
def feishu_hook():
    #判断飞书配置是否开启，如果为0表示关闭
    feishu = con.get("feishu","feishu")
    if feishu == "1":
        #获取json
        data = flask.request.get_json()

        #告警列表长度
        alert_len = len(data['alerts'])

        #获取告警信息中是Firing还是resolved
        alert_status = data['status']



        #循环告警列表,取出告警信息,并存入列表中
        alert_dict = {}
        for i in range(alert_len):
            try:
                #告警名称
                alertname = data['alerts'][i]['labels']['alertname']
                #告警等级
                alert_severity = data['alerts'][i]['labels']['severity']
                #告警主机
                instance = data['alerts'][i]['labels']['instance']
                #告警开始时间
                startsAt = data['alerts'][i]['startsAt']
                #告警结束时间
                endsAt = data['alerts'][i]['endsAt']
                #告警详情
                description = data['alerts'][i]['annotations']['description']
            except KeyError:
                #告警名称
                alertname = data['alerts'][i]['labels']['alertname']
                #告警等级
                alert_severity = data['alerts'][i]['labels']['severity']
                #告警主机
                instance = 'Unkown'
                #告警开始时间
                startsAt = data['alerts'][i]['startsAt']
                #告警结束时间
                endsAt = data['alerts'][i]['endsAt']
                #告警详情
                description = data['alerts'][i]['annotations']['description']

                #判断结束是否为0001-01-01，如果是则不能调用utc转cst函数
                if endsAt == "0001-01-01T00:00:00Z":
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': endsAt, 'instance': instance, 'description': description}
                else:
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': utc_to_cst(endsAt), 'instance': instance, 'description': description}
            else:
                #判断结束是否为0001-01-01，如果是则不能调用utc转cst函数
                if endsAt == "0001-01-01T00:00:00Z":
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': endsAt, 'instance': instance, 'description': description}
                else:
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': utc_to_cst(endsAt), 'instance': instance, 'description': description}

        #获取告警模板
        alert_template = [[{"tag": "text", "text": "告警名称: " },
                           {"tag": "text", "text": alert_dict[i]['alertname']}],
                          [{"tag": "text", "text": "告警等级: "},
                           {"tag": "text", "text": alert_dict[i]['alert_severity']}],
                          [{"tag": "text", "text": "开始时间: "},
                           {"tag": "text", "text": alert_dict[i]['startsAt']}],
                          [{"tag": "text", "text": "结束时间: "},
                           {"tag": "text", "text": alert_dict[i]['endsAt']}],
                          [{"tag": "text", "text": "故障主机: "},
                           {"tag": "text", "text": alert_dict[i]['instance']}],
                          [{"tag": "text", "text": "故障详情: "},
                           {"tag": "text", "text": alert_dict[i]['description']}]]
        resolved_template = [[{"tag": "text", "text": "告警名称: " },
                           {"tag": "text", "text": alert_dict[i]['alertname']}],
                          [{"tag": "text", "text": "告警等级: "},
                           {"tag": "text", "text": alert_dict[i]['alert_severity']}],
                          [{"tag": "text", "text": "开始时间: "},
                           {"tag": "text", "text": alert_dict[i]['startsAt']}],
                          [{"tag": "text", "text": "恢复时间: "},
                           {"tag": "text", "text": alert_dict[i]['endsAt']}],
                          [{"tag": "text", "text": "故障主机: "},
                           {"tag": "text", "text": alert_dict[i]['instance']}],
                          [{"tag": "text", "text": "告警详情: "},
                           {"tag": "text", "text": alert_dict[i]['description']}]]

        #获取到bot_url
        bot_url = con.get("feishu", "bot_url")

        #定义headers头部
        headers = {'Content-Type': 'application/json'}

        if alert_status == "firing":
            #循环告警列表并发送告警
            for i in range(alert_len):
                msg = {
                    "msg_type": "post",
                    "content": {
                        "post": {
                            "zh_cn": {
                                "title": "Prometheus告警信息",
                                "content": alert_template
                            }
                        }
                    }
                }
                res = requests.post(bot_url, headers=headers, json=msg)
        elif alert_status == "resolved":
            #循环告警列表并发送告警
            for i in range(alert_len):
                msg = {
                    "msg_type": "post",
                    "content": {
                        "post": {
                            "zh_cn": {
                                "title": "Prometheus告警恢复信息",
                                "content": resolved_template
                            }
                        }
                    }
                }
                res = requests.post(bot_url, headers=headers, json=msg)
        return json.dumps({"msg":"request OK"}, ensure_ascii=False)
    else:
        print({"msg_error": "请检查飞书配置是否打开！"})
        return json.dumps({"msg":"配置错误，请检查飞书配置是否打开！"}, ensure_ascii=False)


@server.route('/api/dingding', methods=['post'])
def dingding_hook():
    #获取json数据
    data = flask.request.get_json()
    
    #判断dingding配置是否开启
    dingding = con.get('dingding', 'dingding')
    if dingding == '1':
        #获取json
        data = flask.request.get_json()

        #告警列表长度
        alert_len = len(data['alerts'])

        #获取告警信息中是Firing还是resolved
        alert_status = data['status']



        #循环告警列表,取出告警信息,并存入列表中
        alert_dict = {}
        for i in range(alert_len):
            try:
                #告警名称
                alertname = data['alerts'][i]['labels']['alertname']
                #告警等级
                alert_severity = data['alerts'][i]['labels']['severity']
                #告警主机
                instance = data['alerts'][i]['labels']['instance']
                #告警开始时间
                startsAt = data['alerts'][i]['startsAt']
                #告警结束时间
                endsAt = data['alerts'][i]['endsAt']
                #告警详情
                description = data['alerts'][i]['annotations']['description']
            except KeyError:
                #告警名称
                alertname = data['alerts'][i]['labels']['alertname']
                #告警等级
                alert_severity = data['alerts'][i]['labels']['severity']
                #告警主机
                instance = 'Unkown'
                #告警开始时间
                startsAt = data['alerts'][i]['startsAt']
                #告警结束时间
                endsAt = data['alerts'][i]['endsAt']
                #告警详情
                description = data['alerts'][i]['annotations']['description']

                #判断结束是否为0001-01-01，如果是则不能调用utc转cst函数
                if endsAt == "0001-01-01T00:00:00Z":
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': endsAt, 'instance': instance, 'description': description}
                else:
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': utc_to_cst(endsAt), 'instance': instance, 'description': description}
            else:
                #判断结束是否为0001-01-01，如果是则不能调用utc转cst函数
                if endsAt == "0001-01-01T00:00:00Z":
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': endsAt, 'instance': instance, 'description': description}
                else:
                    #加入字典中，等待发送告警消息
                    alert_dict[i] = {'alertname': alertname, 'alert_severity': alert_severity, 'startsAt': utc_to_cst(startsAt), 'endsAt': utc_to_cst(endsAt), 'instance': instance, 'description': description}

        #获取告警模板
        alert_template = '### Prometheus告警信息  \n  告警名称：{}  \n  告警等级：{}  \n  开始时间：{}  \n  结束时间：{}  \n  故障主机：{}  \n  告警详情：{}'.format(alert_dict[i]['alertname'], alert_dict[i]['alert_severity'], alert_dict[i]['startsAt'], alert_dict[i]['endsAt'], alert_dict[i]['instance'], alert_dict[i]['description'])
        resolved_template = '### Prometheus告警恢复信息  \n  告警名称：{}  \n  告警等级：{}  \n  开始时间：{}  \n  恢复时间：{}  \n  故障主机：{}  \n  告警详情：{}'.format(alert_dict[i]['alertname'], alert_dict[i]['alert_severity'], alert_dict[i]['startsAt'], alert_dict[i]['endsAt'], alert_dict[i]['instance'], alert_dict[i]['description'])

        #获取到bot_url
        bot_url = con.get("dingding", "bot_url")

        #定义headers头部
        headers = {'Content-Type': 'application/json;charset=utf-8'}

        if alert_status == "firing":
            #循环告警列表并发送告警
            for i in range(alert_len):
                msg = {
                    "msgtype" : "markdown",
                    "markdown": {
                        "title": "Pormetheus告警信息",
                        "text" : alert_template
                    }
                    # "at": {
                    # "atMobiles": [
                    #     ""
                    # ],
                    # "isAtAll": "false"
                    # }
                }
                res = requests.post(bot_url, json.dumps(msg),headers=headers)
        elif alert_status == "resolved":
            #循环告警列表并发送告警
            for i in range(alert_len):
                msg = {
                    "msgtype" : "markdown",
                    "markdown": {
                        "title": "Pormetheus告警恢复信息",
                        "text" : resolved_template
                    }
                    # "at": {
                    # "atMobiles": [
                    #     ""
                    # ],
                    # "isAtAll": "false"
                    # }
                }
                res = requests.post(bot_url, headers=headers, json=msg)
        return json.dumps({"msg":"request OK"}, ensure_ascii=False)
    else:
        print({"msg_error": "请检查dingding配置是否打开！"})
        return json.dumps({"msg":"配置错误，请检查dingding配置是否打开！"}, ensure_ascii=False)


#api健康检查接口
@server.route('/api/health', methods=['get'])
def health():
    return json.dumps({'status': 'OK'})