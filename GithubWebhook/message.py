import GithubWebhook
import OlivOS
import threading

bot_dict = {}

def set_bot_dict(bot_info_dict):
    global bot_dict
    bot_dict.update(bot_info_dict)

def create_fake_event(bot_hash):
    global bot_dict
    plugin_event = OlivOS.API.Event(
        OlivOS.contentAPI.fake_sdk_event(
            bot_info = bot_dict[bot_hash],
            fakename = GithubWebhook.data.PLUGIN_NAME
        ),
        GithubWebhook.main.logger.log           # 框架原生 log 函数
    )
    return plugin_event


class GithubEvent:
    def __init__(self, event, data):
        self.event = event
        self.data = data
        self._thread = None
        if event == "push":
            self._thread = threading.Thread(target=self.push, daemon=False)
        elif event == "issues":
            self._thread = threading.Thread(target=self.push, daemon=False)

    def start(self):
        if self._thread is not None:
            self._thread.start()

    def push(self):
        pass

    def issues(self):
        pass
