from urllib import request

import chardet
import requests
from flask import Flask, Response, Request, jsonify, json
from werkzeug.routing import BaseConverter
import struct

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


# 我这里先默认向8080发请求,port之后会改

@app.route('/index.html')
def simple():
    html = requests.get('http://127.0.0.1:8080/index.html')
    return html.content


@app.route('/swfobject.js')
def simple1():
    html = requests.get('http://127.0.0.1:8080/swfobject.js')
    return html.content


@app.route('/StrobeMediaPlayback.swf')
def simple2():
    html = requests.get('http://127.0.0.1:8080/StrobeMediaPlayback.swf')
    return html.content


@app.route('/vod/big_buck_bunny.f4m')
def simple3():
    html = requests.get('http://127.0.0.1:8080/vod/big_buck_bunny_nolist.f4m')
    return html.content

@app.route('/vod/<regex("[0-9]{2,4}"):bit_rate>Seg<regex("[0-9]{0,}"):seg>-Frag<regex("[0-9]+$"):frag>')
def simple4(bit_rate,seg, frag):
    html = requests.get('http://127.0.0.1:8080/vod/'+bit_rate+'Seg'+seg+'-Frag'+frag)
    return html.content



if __name__ == '__main__':
    app.run(port=8999)
