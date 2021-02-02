from flask import Flask
from flask import render_template
import requests
import json
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Taipei")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

server_ips = [
    "140.118.127.79",
    "140.118.127.81",
    "140.118.127.87",
    "140.118.127.90",
]


@app.route('/')
def hello_world():
    servers = list()
    now = datetime.now(tz=tz).strftime("%Y-%m-%d %T")
    for ip in server_ips:
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

    context = {"now": now, "servers": servers}
    return render_template("index.html", **context)
