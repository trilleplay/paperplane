from flask import Flask, render_template, Response
import yaml
app = Flask(__name__)

with open("config.yml") as file:
    web_config = yaml.load(file, Loader=yaml.FullLoader)

@app.route("/")
def index():
    return render_template("index.html", invite_url=web_config["web"]["bot_invite"])

@app.route("/added")
def index():
    return render_template("index.html", invite_url=web_config["web"]["bot_invite"])

@app.route("/riot.txt")
def riot_verify():
    return Response(web_config["web"]["riot_games_key"], mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
