import sys,os,configparser
# 将当前目录加入模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 将项目根目录加入模块搜索路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置环境变量
os.environ['PROJECT_PATH'] = os.path.dirname(os.path.abspath(__file__))

from lib.api import server

#创建配置文件对象
file = '../config/config.ini'
con = configparser.ConfigParser()
con.read(file, encoding='utf-8')

#读取系统变量
SERVER_PORT = os.environ.get("SERVER_PORT")
if SERVER_PORT == None:
    SERVER_PORT = con.get('global', 'server_port')

#启动命令
#gunicorn Alertmanager-repeater:server -w 6 -b 0.0.0.0:$SERVER_PORT


# if __name__ == '__main__':
#     server.run(
#         host='0.0.0.0',
#         port=SERVER_PORT,
#     )