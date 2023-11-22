from flask import Flask, request, jsonify, render_template
from pprint import pprint
import json
from .PyOSCQueryNode import PyOSCQueryRootNode, PyOSCQueryNode
from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo
from .sockethelper import find_available_port
import socket
import atexit

SERVICE_UDP = "_osc._udp.local."
SERVICE_TCP = "_oscjson._tcp.local."



class PyOSCQuery:
    def __init__(self, port=8000, host='localhost', name='PyOSCQuery'):
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        self.name = name
        self.host = host
        self.port = port
        self.root_node = PyOSCQueryRootNode()
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/debug', 'debug', self.debug)
        # self.app.after_request(self.after_request)
        # check if hostinfo is good
        
        self.hostinfo = None
        self.zc = Zeroconf()
        self.service_info = None

    def index(self):
        #if query is HOST_INFO return hostinfo
        if request.query_string.decode('utf-8') == 'HOST_INFO':
            # print request contents
            pprint(request.__dict__)
            return jsonify(self.hostinfo)

        if request.query_string.decode('utf-8') == 'explorer':
            return render_template('OSCQueryExplorer.html')

        if request.method == 'GET':
            response = self.app.response_class(
                    response=str(self.root_node),
                    status=200,
                    mimetype='application/json'
            )
            return response

    # def after_request(self, response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     return response

    def debug(self):
        return str(self.root_node)

    def create_service_info(self):
        self.port = find_available_port('both',self.port)
        self.hostinfo = {
            "NAME": self.name,
            "EXTENSIONS": {
                "ACCESS": True,
                "CLIPMODE": False,
                "RANGE": True,
                "TYPE": True,
                "VALUE": True
            },
            "OSC_IP": "127.0.0.1",
            "OSC_PORT": self.port,
            "OSC_TRANSPORT": "UDP"
        }
        #self.osc_udp_port = find_available_port('udp',self.hostinfo["OSC_PORT"])
        self.service_info =[
            ServiceInfo(
                SERVICE_UDP,
                f"_{self.name}."+SERVICE_UDP,
                addresses=[socket.inet_aton("127.0.0.1")],
                port=self.port,
                properties={},
                server="localhost.local."
            ),
            ServiceInfo(
                SERVICE_TCP,
                f"_{self.name}."+SERVICE_TCP,
                addresses=[socket.inet_aton("127.0.0.1")],
                port=self.port,
                properties={},
                server="localhost.local."
            )
        ]  
        
    def stop_zc(self):
        self.zc.close()

    def run(self):
        self.create_service_info()
        atexit.register(self.stop_zc)
        for info in self.service_info:
            Zeroconf.register_service(self.zc, info)
        self.app.run(host=self.host, port=self.port, debug=True)

