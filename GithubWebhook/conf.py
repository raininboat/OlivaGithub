import os
import uuid
import GithubWebhook
import json

conf_dict = {}

def releaseDir(path):
    "创建目录"
    if not os.path.isdir(path):
        os.mkdir(path)

def load_data(root_path=None):
    global conf_dict
    if root_path is None:
        root_path = os.path.abspath("./plugin/data")
    releaseDir(root_path+GithubWebhook.data.file_dir_path)
    get_access_tocken(root_path)
    GithubWebhook.main.logger.debug(conf_dict["access_tocken"])
    get_conf(root_path)
    GithubWebhook.main.logger.debug(conf_dict)

def get_conf(path):
    global conf_dict
    file_path = path + GithubWebhook.data.file_conf_path
    if not os.path.isfile(file_path):
        default_conf = GithubWebhook.data.default_conf
        with open(file_path, "wt", encoding="utf-8") as file:
            file.write(json.dumps(default_conf, ensure_ascii=False, indent=4))
        conf_dict.update(default_conf)
    else:
        try:
            with open(file_path, "rt", encoding="utf-8") as file:
                conf_data = json.loads(file.read())
            conf_dict.update(conf_data)
        except Exception as err:
            GithubWebhook.main.logger.error("Github Webhook 插件发生错误！读取 conf 内容失败，使用默认")

def get_access_tocken(path):
    global conf_dict
    file_path = path + GithubWebhook.data.file_access_tocken_path
    if not os.path.isfile(file_path):
        with open(file_path, "wt", encoding="utf-8") as file:
            file.write(uuid.uuid4().hex)
    with open(file_path, "rt", encoding="utf-8") as file:
        access_tocken = file.read().strip()
    conf_dict["access_tocken"] = access_tocken
