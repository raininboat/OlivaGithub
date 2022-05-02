import GithubWebhook
import threading
import hmac
from flask import Flask
from flask import current_app
from flask import request
from flask import make_response
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
                    res = make_response("What the hell are you doing?")
                    res.status = 405
                    return res
                elif request.method == "POST":
                    with request:
                        x_sign = request.headers.get("X-Hub-Signature-256",default="",type=str)
                        hash_obj = hmac.new(self.conf["access_tocken"].encode("utf-8"),msg=request.get_data(),digestmod="sha256")
                        local_sign = f"sha256={hash_obj.hexdigest()}"
                        if not hmac.compare_digest(x_sign,local_sign):
                            res = make_response("Signature Error!")
                            res.status = 401
                            self.log.debug("签名错误！请检查 GitHub Webhook Secret 设置情况")       # 签名失败的 log 等级设置为 debug, 正常状态屏蔽
                            return res
                        if request.content_type != "application/json":
                            res = make_response("Please use 'application/json' content type")
                            res.status = 400
                            self.log.error("Github Webhook 中 'content type' 应设置为 'application/json'")
                            return res
                        event = request.headers.get("X-GitHub-Event", default="", type=str)
                        data = request.get_json()
                        
                        
                        return "OK"

    def run(self):
        self.set_config()
        if self.conf["debug"]:
            self.app.run("0.0.0.0", self.conf["port"])
        else:
            server = pywsgi.WSGIServer(("0.0.0.0", self.conf["port"]), self.app, log=None)
            server.serve_forever()
        # self.app.run()

    def start(self):
        self._thread.start()

def run_server():
    server = FlaskServer(conf=GithubWebhook.conf.conf_dict)
    server.start()
