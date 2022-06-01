import requests
from flask import Flask, Response, request, jsonify, json
from werkzeug.routing import BaseConverter
import time
import sys
from threading import Thread
from time import sleep


app = Flask(__name__)
finish_flag = False
Tput = {}
alpha = 0.0
bitrate = []
end_t = 0
listen_port = 0
dns_port = 0
need_dns = True
default_port = 0

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter


@app.route('/seriouslykill')
def seriouslykill():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Shutting down..."


@app.route('/index.html')
def simple():
    if need_dns:
        port = int(requests.get('http://127.0.0.1:'+str(dns_port)+'/getserver').content)
        url = 'http://127.0.0.1:' + str(port) + '/index.html'
    else:
        url = 'http://127.0.0.1:' + str(default_port) + '/index.html'
    html = requests.get(url)
    return html.content


@app.route('/swfobject.js')
def simple1():
    if need_dns:
        port = int(requests.get('http://127.0.0.1:'+str(dns_port)+'/getserver').content)
        url = 'http://127.0.0.1:' + str(port) + '/swfobject.js'
    else:
        url = 'http://127.0.0.1:' + str(default_port) + '/swfobject.js'
    html = requests.get(url)
    return html.content


@app.route('/StrobeMediaPlayback.swf')
def simple2():
    if need_dns:
        port = int(requests.get('http://127.0.0.1:'+str(dns_port)+'/getserver').content)
        url = 'http://127.0.0.1:' + str(port) + '/StrobeMediaPlayback.swf'
    else:
        url = 'http://127.0.0.1:' + str(default_port) + '/StrobeMediaPlayback.swf'
    html = requests.get(url)
    return html.content


@app.route('/vod/big_buck_bunny.f4m')
def simple3():
    if need_dns:
        port = int(requests.get('http://127.0.0.1:'+str(dns_port)+'/getserver').content)
        url = 'http://127.0.0.1:' + str(port) + '/vod/big_buck_bunny_nolist.f4m'
        url1 = 'http://127.0.0.1:' + str(port) + '/vod/big_buck_bunny.f4m'
    else:
        url = 'http://127.0.0.1:' + str(default_port) + '/vod/big_buck_bunny_nolist.f4m'
        url1 = 'http://127.0.0.1:' + str(default_port) + '/vod/big_buck_bunny.f4m'
    html = requests.get(url)
    test = requests.get(url1)
    # print(test.content.decode())
    sw = test.content.decode().split('bitrate')
    if len(bitrate) < 4:
        for i in range(1, 5):
            temp = sw[i][2]
            j = 3
            while sw[i][j] != '"':
                temp += sw[i][j]
                j = j + 1
            bitrate.append(int(temp))
    for i in bitrate:
        print(i)
    return html.content


@app.route('/vod/<regex("[0-9]{2,4}"):bit_rate>Seg<regex("[0-9]{0,}"):seg>-Frag<regex("[0-9]+$"):frag>')
def simple4(bit_rate,seg, frag):
    if need_dns:
        port = int(requests.get('http://127.0.0.1:'+str(dns_port)+'/getserver').content)
        url = 'http://127.0.0.1:' + str(port) + '/vod/'
    else:
        port = int(default_port)
        url = 'http://127.0.0.1:' + str(default_port) + '/vod/'
    print(str(port))

    for i in range(len(bitrate)-1,-1,-1):
        if Tput[port] > 1.5*bitrate[i]:
            bit_rate = bitrate[i]
            break
        if i == 0:
            bit_rate = bitrate[0]
    print('Current bit rate is : '+ str(bit_rate))

    start_local_time = time.localtime()
    # print(start_local_time)

    global end_t
    start_t = time.time()
    html = requests.get(url+str(bit_rate)+'Seg'+seg+'-Frag'+frag)
    end_t = time.time()

    duration = end_t - start_t

    len_ = len(html.content)
    # print('content length is: '+str(len(html.content)))
    # print('end - start: '+str(end_t-start_t))
    tput = (float(len_) / duration * 8 )/ 1000
    Tput[port] = alpha * Tput[port] + (1.0 - alpha) * tput
    print('EWMA is ' + str(Tput[port]))

    # time_str = str(time.strftime("%Y-%m-%d %H:%M:%S",start_local_time))
    time_str = start_t

    file.write('{time} {duration} {tput} {avg_tput} {bitrate} {server_port} {chunkname}\n'.format(time=time_str,
                                                                                                  duration=duration,
                                                                                                  tput=tput,
                                                                                                  avg_tput=Tput[port],
                                                                                                  bitrate=bit_rate,
                                                                                                  server_port=port,
                                                                                                  chunkname=str(
                                                                                                      seg + '-' + frag)))
    
    if int(seg) == 102 and int(frag) == 596:
        finish_flag = True
    file.flush()                                                                                  
    return html.content

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def A():
    global end_t
    while(True):
        sleep(1)
        # print('---------------------------')
        # print('current time is ' + str(time.time()))
        # print('end_t is ' + str(end_t))
        # print('---------------------------')
        if time.time() - end_t > 60 or finish_flag:
            print('shutdown-------------------')
            file.close()
            requests.get('http://127.0.0.1:'+str(dns_port)+'/release_port:'+str(default_port))
            requests.get('http://127.0.0.1:'+str(listen_port)+'/seriouslykill')
            break
            sys.exit(0)

if __name__ == '__main__':
    log_name = sys.argv[1]
    file = open(log_name, 'w', encoding='utf-8')
    alpha = float(sys.argv[2])
    listen_port = sys.argv[3]
    dns_port = sys.argv[4]
    
    # print('http://127.0.0.1:'+str(dns_port)+'/getallservers')
    allservers = requests.get('http://127.0.0.1:'+str(dns_port)+'/getallservers').content.decode().split(',')
    
    print(allservers)
    for i in allservers:
        Tput[int(i)] = 0.0

    print(Tput)  

    if len(sys.argv) > 5:
        need_dns = False
        default_port = sys.argv[5]
        # print(default_port)
        Tput[int(default_port)] = 0.0
        p = requests.get('http://127.0.0.1:'+str(dns_port)+'/occupy_port:' + str(default_port)).content.decode()
        # print(p)
    else:
        need_dns = True

    end_t = time.time()
    A()

    server = app.run(port=listen_port)
    # start_server()

    # python3 home/CS305-proj/docker_setup/netsim/netsim.py servers start -s home/CS305-proj/docker_setup/netsim/servers/2servers 

    # python3 home/CS305-proj/starter_proxy/proxy.py aaa 0.5 8899 8888 8080
    # python3 home/CS305-proj/starter_proxy/proxy.py aaa 0.5 8898 8888 8080


    # python3 netsim.py onelink start -s servers/2servers
    # python3 netsim.py onelink run -e topology/onelink/onelink.events
    # python3 netsim.py onelink stop 


# python3 /home/CS305-proj/docker_setup/netsim/netsim.py onelink start -l /home/CS305-proj/docker_setup/netsim/log.txt

# python3 /home/CS305-proj/docker_setup/netsim/netsim.py onelink run -e /home/CS305-proj/docker_setup/netsim/topology/onelink/onelink.events


# python3 /home/CS305-proj/starter_proxy/proxy.py /home/CS305-proj/starter_proxy/aaa 0.5 8899 8888 15641