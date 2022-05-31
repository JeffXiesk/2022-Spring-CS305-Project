import sys
from werkzeug.routing import BaseConverter
from flask import Flask, Response, Request, jsonify, json

app = Flask(__name__)

cnt = 0
port_num = 0
current_use = 0
port_used = {}


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

# get a server not used by default port request
@app.route('/getserver')
def get_serve():
    global cnt
    cnt = cnt + 1
    res = cnt % port_num
    while port_used[res]:
        cnt = cnt + 1
        res = cnt % port_num
    return servers[res]


# set a server used by default port request
@app.route('/occupy_port:<regex("[0-9]+"):port_name>')
def set_occupied(port_name):
    port_used[port_name] = True


# release a server used by default port request
@app.route('/release_port:<regex("[0-9]+"):port_name>')
def set_released(port_name):
    port_used[port_name] = False


if __name__ == '__main__':
    # print(1)
    with open(sys.argv[1]) as f:
        servers = f.readlines()
    port_num = len(servers)
    for i in range(port_num):
        servers[i] = servers[i].strip('\n')
        port_used[servers[i]] = False
    print(servers)
    app.run(port=8888)