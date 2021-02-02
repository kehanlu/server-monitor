from flask import Flask
from flask import render_template
import requests
import json
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

server_ips = [
    "140.118.127.87"
]


@app.route('/')
def hello_world():
    servers = list()
    for ip in server_ips:
        resp = json.loads(requests.get(f"http://{ip}:23333").text)
        print(resp)
        resp["ip"] = ip
        servers.append(resp)

    context = {"servers": servers}
    return render_template("index.html", **context)
