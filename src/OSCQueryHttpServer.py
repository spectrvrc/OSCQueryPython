from flask import Flask, request, jsonify, render_template
from pprint import pprint
import json
from OSCQueryNode import OSCQueryRootNode, OSCQueryNode


class PyOSCQuery:
    def __init__(self, port=8000, host='localhost'):
        self.app = Flask(__name__)
        self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        self.host = host
        self.port = port
        self.root_node = OSCQueryRootNode()
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/debug', 'debug', self.debug)
        # check if hostinfo is good
        with open('hostinfo.json') as f:
            self.hostinfo = json.load(f)

    def index(self):
        #if query is HOST_INFO return hostinfo
        if request.query_string.decode('utf-8') == 'HOST_INFO':
            return jsonify(self.hostinfo)

        if request.query_string.decode('utf-8') == 'explorer':
            return render_template('OSCQueryExplorer.html')

        if request.method == 'GET':
            return str(self.root_node)

    def debug(self):
        return str(self.root_node)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)
