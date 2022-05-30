import sys
from flask import Flask, Response, Request, jsonify, json

app = Flask(__name__)

cnt = 0
port_num = 0
current_use = 0

@app.route('/getserver')
def getserve():
    global cnt
    cnt = cnt + 1
    res = cnt % port_num
    return servers[res]

if __name__ == '__main__':
    print(1)
    with open(sys.argv[1]) as f:
        servers = f.readlines()
    port_num = len(servers)
    for i in range(port_num):
        servers[i] = servers[i].strip('\n')
    print(servers)
    app.run(port=8888)

