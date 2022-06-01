import requests
from flask import Flask, Response
if __name__ == '__main__':
    for i in range(100):
        response = int(requests.get('http://127.0.0.1:8888/getserver').content)
        print(int(response))

# python3 /home/CS305-proj/starter_proxy/dns.py /home/CS305-proj/docker_setup/netsim/servers/2servers