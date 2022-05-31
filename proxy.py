# from urllib import request

import requests
from flask import Flask, Response, request, jsonify, json
from werkzeug.routing import BaseConverter
import struct
import time
import sys

app = Flask(__name__)
Tput = {}
alpha = 0.0
bitrate = []

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


# 我这里先默认向8080发请求,port之后会改

@app.route('/index.html')
def simple():
    port = int(requests.get('http://127.0.0.1:8888/getserver').content)
    url = 'http://127.0.0.1:' + str(port) + '/index.html'
    print(str(port))
    html = requests.get(url)
    return html.content


@app.route('/swfobject.js')
def simple1():
    port = int(requests.get('http://127.0.0.1:8888/getserver').content)
    url = 'http://127.0.0.1:' + str(port) + '/swfobject.js'
    print(str(port))
    html = requests.get(url)
    return html.content


@app.route('/StrobeMediaPlayback.swf')
def simple2():
    port = int(requests.get('http://127.0.0.1:8888/getserver').content)
    url = 'http://127.0.0.1:' + str(port) + '/StrobeMediaPlayback.swf'
    print(str(port))
    html = requests.get(url)
    return html.content


@app.route('/vod/big_buck_bunny.f4m')
def simple3():
    port = int(requests.get('http://127.0.0.1:8888/getserver').content)
    url = 'http://127.0.0.1:' + str(port) + '/vod/big_buck_bunny_nolist.f4m'
    url1 = 'http://127.0.0.1:' + str(port) + '/vod/big_buck_bunny.f4m'
    html = requests.get(url)
    test = requests.get(url1)
    sw = test.content.decode().split('bitrate')
    for i in range(len(sw)):
        if i == 1:
            bitrate.append(int(sw[i][2:3]))
        if i == 2 or i == 3:
            bitrate.append(int(sw[i][2:4]))
        if i == 4:
            bitrate.append(int(sw[i][2:5]))
    for i in bitrate:
        print(i)
    return html.content

@app.route('/vod/<regex("[0-9]{2,4}"):bit_rate>Seg<regex("[0-9]{0,}"):seg>-Frag<regex("[0-9]+$"):frag>')
def simple4(bit_rate,seg, frag):
    port = int(requests.get('http://127.0.0.1:8888/getserver').content)
    url = 'http://127.0.0.1:' + str(port) + '/vod/'
    print(str(port))
    start_t = time.time()
    html = requests.get(url+bit_rate+'Seg'+seg+'-Frag'+frag)
    end_t = time.time()
    len_ = len(html.content)
    Tput[port] = (alpha*Tput[port] + (1.0-alpha)*float(len_)/(end_t-start_t))*8
    print(Tput[port])

    return html.content


if __name__ == '__main__':
    while True:
        port = int(requests.get('http://127.0.0.1:8888/getserver').content)
        if port in Tput:
            break
        else:
            Tput[port] = 0.0
            
    alpha = float(sys.argv[2])
    
    app.run(port=8999)
