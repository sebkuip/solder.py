import flask
import hashlib
import os
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv(".env")

api_key = getenv("API_KEY")
mirror_url = getenv("URL")

app = flask.Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def index():
    return flask.jsonify({"error": "No endpoint specified"})

@app.route("/api/")
def api():
    return flask.jsonify({"api":"solder.py","version":"v0.0.1a","stream":"DEV"})

@app.route("/api/verify")
def verify(key: str = None):
    return flask.jsonify({"error": "No API key provided."})

@app.route("/api/verify/<key>")
def verify_key(key: str = None):
    if key == api_key:
        return flask.jsonify({"valid":"Key validated.", "name": "API KEY", "created_at": "1970-01-01T00:00:00+00:00"})
    else:
        return flask.jsonify({"error":"Invalid key provided."})

@app.route("/api/modpack")
def modpack():
    modpacks: dict = {}
    for filename in os.listdir("./modpacks"):
        with open(f"modpacks/{filename}", "r") as f:
            info = json.load(f)
            if flask.request.args.get("include") == "full":
                fulldata: dict = {}
                fulldata["name"]  = filename.removesuffix(".json")
                fulldata["display_name"] = info["display_name"]
                fulldata["url"] = info["url"]
                fulldata["icon"] = info["icon"]
                fulldata["icon_md5"] = info["icon_md5"]
                fulldata["logo"] = info["logo"]
                fulldata["logo_md5"] = info["logo_md5"]
                fulldata["background"] = info["background"]
                fulldata["background_md5"] = info["background_md5"]
                fulldata["recommended"] = info["recommended"]
                fulldata["latest"] = info["latest"]
                builds: list = []
                for version in info["builds"]:
                    builds.append(version["version"])
                fulldata["builds"] = builds
                modpacks[filename.removesuffix('.json')] = fulldata
            else:
                modpacks[filename.removesuffix('.json')] = info["display_name"]
    return flask.jsonify({
        "modpacks": modpacks,
        "mirror_url": mirror_url
    })

@app.route("/api/modpack/<slug>")
def modpack_slug(slug: str):
    try:
        with open(f"modpacks/{slug}.json", "r") as f:
            info = json.load(f)
            modpack: dict = {}

            modpack["name"]  = slug
            modpack["display_name"] = info["display_name"]
            modpack["url"] = info["url"]
            modpack["icon"] = info["icon"]
            modpack["icon_md5"] = info["icon_md5"]
            modpack["logo"] = info["logo"]
            modpack["logo_md5"] = info["logo_md5"]
            modpack["background"] = info["background"]
            modpack["background_md5"] = info["background_md5"]
            modpack["recommended"] = info["recommended"]
            modpack["latest"] = info["latest"]
            builds = []
            for version in info["builds"]:
                builds.append(version["version"])
            modpack["builds"] = builds
            return flask.jsonify(modpack)
    except FileNotFoundError:
        return flask.jsonify({"error": "Modpack does not exist/Build does not exist"})

@app.route("/api/modpack/<slug>/<build>")
def modpack_slug_build(slug: str, build: str):
    return flask.jsonify({
        "minecraft":"1.5.1",
        "minecraft_md5":"5c1219d869b87d233de3033688ec7567",
        "forge":None,
        "mods":[
            {
            "name":"basemods",
            "version":"tekkitmain-v1.0.2",
            "md5":"842658e9a8a03c1210d563be1b7d09f5",
            "url":"http:\/\/mirror.technicpack.net\/Technic\/mods\/basemods\/basemods-tekkitmain-v1.0.2.zip"
            },
            {
            "name":"balkonsweaponmod",
            "version":"v1.11",
            "md5":"016bb3edb2fa11c7212fd4cf2504e260",
            "url":"http:\/\/mirror.technicpack.net\/Technic\/mods\/balkonsweaponmod\/balkonsweaponmod-v1.11.zip"
            }
        ]
    })

@app.route("/api/mod")
def mod():
    return flask.jsonify({
        "error": "No mod requested/Mod does not exist/Mod version does not exist"
    })

@app.route("/api/mod/<name>")
def mod_name(name: str):
    return flask.jsonify({
        "name": "testmod",
        "pretty_name": "TestMod",
        "author": "Technic",
        "description": "This is a test mod for Solder",
        "link": "http://solder.io",
        "donate": None,
        "versions": [
            "0.1"
        ]
    })

@app.route("/api/mod/<name>/<version>")
def mod_name_version(name: str, version: str):
    return flask.jsonify({
        "md5": "fb6582e4d9c9bc208181907ecc108eb1",
        "url": "http://technic.pagefortress.com/mods/testmod/testmod-0.1.zip"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0")