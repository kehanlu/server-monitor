from flask import Flask
from flask import render_template
import requests
import json
from datetime import datetime
import pytz
from config import CONFIG

tz = pytz.timezone("Asia/Taipei")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

SITE_TITLE = CONFIG.get("site_title", "Server status")
TOP_MESSAGE = CONFIG.get("top_message", "Hello world")

if CONFIG.get("server_ips") is None:
    raise ValueError()
SERVER_IPS = CONFIG.get("server_ips")


@app.route('/')
def server():
    servers = list()
    now = datetime.now(tz=tz).strftime("%Y-%m-%d %T")
    for ip in SERVER_IPS:
        resp = requests.get(f"http://{ip}:23333")
        if resp.status_code != 200:
            data = {
                "ip": ip,
                "active": False
            }
        else:
            data = json.loads(resp.text)
            data["ip"] = ip
            data["active"] = True
        servers.append(data)

    context = {"title": SITE_TITLE,
               "top_message": TOP_MESSAGE,
               "now": now,
               "servers": servers}
    return render_template("index.html", **context)
