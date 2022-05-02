import GithubWebhook
import threading
from flask import Flask
from flask import current_app
from flask import request
from gevent import pywsgi

server = None
class FlaskServer:
    def __init__(self, conf) -> None:
        self.namespace = __name__
        self.conf = conf
        self.log = GithubWebhook.main.logger
        self.app = Flask(self.namespace)
        self._thread = threading.Thread(target=self.run, daemon=True)

    def set_config(self):
        with self.app.app_context():
            @current_app.route(self.conf["url_endpoint"],methods=["POST", "GET"])
            def flask_server_run():
                if request.method == "GET":
                    return "What are you doing?"
                elif request.method == "POST":
                    self.log.debug(request.headers)
                    self.log.debug("==============================")
                    self.log.debug(request.content_type)
                    self.log.debug(request.get_json())
                    self.log.debug(request.get_data())
                    return "200"

    def run(self):
        self.set_config()
        server = pywsgi.WSGIServer(("127.0.0.1", self.conf["port"]), self.app)
        server.serve_forever()
        # self.app.run()

    def start(self):
        self._thread.start()

def run_server():
    server = FlaskServer(conf=GithubWebhook.conf.conf_dict)
    server.start()
