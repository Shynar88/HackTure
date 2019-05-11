import json
import os

from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS

import googleapiclient.discovery
import requests


app = Flask(__name__)
CORS(app)

api = Api(app)


@app.route("/", methods=["POST"])
def get_video_list():
    data = request.get_json()
    print(data)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCDsSS0qWdJrx9Xmdbuk5FWP-ROzpzRGCw"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    query = youtube.search().list(
        part="snippet",
        q=data["query"]
    )

    response = query.execute()

    return json.dumps(response)


@app.route("/subtitles", methods=["GET"])
def get_video_subtitles():
    q = request.get_json()
    print("request.get_json() =", q)

    r = requests.get("https://subtitles-for-youtube.p.rapidapi.com/subtitles/%s?translated=None&type=None" % q["videoID"],
                     headers={"X-RapidAPI-Host": "subtitles-for-youtube.p.rapidapi.com",
                              "X-RapidAPI-Key": "042f3fd40bmsh299a3d264e6259ep190110jsnf075030f8fec"})
    return r.json()


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
