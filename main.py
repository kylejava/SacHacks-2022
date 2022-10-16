import requests
import os
import json
import string
import random
import sys
from pprint import pprint
from flask import Flask, render_template, flash, request, redirect
import webbrowser
import base64
app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
SCOPE = os.environ.get("SCOPE")
ENCODEDSTRING = os.environ.get("ENCODEDSTRING")


@app.route('/', methods = ["GET", "POST"])
def home():
    print(CLIENT_ID)
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    state = string.ascii_lowercase
    state = ''.join(random.choice(state) for i in range(10))
    auth_url = "https://accounts.spotify.com/authorize?response_type=code&redirect_uri={}&scope={}&client_id={}&state={}".format(REDIRECT_URI,SCOPE,CLIENT_ID,state)
    return redirect(auth_url)

@app.route('/callback/' , methods = ['GET', ' POST'])
def callback():
    token = request.args['code']
    state = request.args['state']
    params = {
        "code":token,
        "redirect_uri":REDIRECT_URI,
        "grant_type":"authorization_code"
    }
    HEADERS = {
    "Authorization": "Basic {}".format(ENCODEDSTRING),
    "Content-Type": "application/x-www-form-urlencoded"
    }

    auth_url="https://accounts.spotify.com/api/token"
    requested_data = requests.post(auth_url, data=params, headers = HEADERS)
    final_data = requested_data.json()
    print(final_data)
    if("error" in final_data):
        return redirect('/')
    return display_data(final_data['access_token'])

@app.route('/display',methods = ['GET', 'POST'])
def display(my_token):
    user_ = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=50&offset=1", headers=HEADERS)
    user_ = user_.json()
    tracks = []
    for item in user_['items']:
        track = item['album']
        if(track['name'] + ' - ' + track['artists'][0]['name']) in tracks:
            print("")
        else:
            album = {
                "name": track['artists'][0]['name'],
                "album": track['name'],
                "image": track['images'][0]['url'],
                "link": track["artists"][0]["external_urls"]["spotify"]
            }
            tracks.append(album)
            if(len(tracks) == 8):
                break





    return render_template("index.html")



if __name__=="__main__":
    app.run(debug=True)
