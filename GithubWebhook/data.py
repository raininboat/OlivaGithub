import GithubWebhook

PLUGIN_NAME = "OlivaGithub"

default_conf = {
    "port" : 7000,
    "url_endpoint" : "/GithubWebhook/api",
    "host_name" : "这里填写你的 ip 或者域名",
    "debug" : False,
}

file_dir_path = "/GithubWebhook"
file_conf_path = "/GithubWebhook/conf.json"
file_access_tocken_path = "/GithubWebhook/ACCESS_TOCKEN.txt"        # 为方便普通用户直接打开，添加 .txt 后缀

url_tamplate = "http://{name}:{default_port}{url_endpoint}?access_tocken={access_tocken}"
