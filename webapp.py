import sqlite3
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import requests
import json

app = Flask(__name__)

DB_GET_CLIPS = 'select name, title, description from clips'
DB_MAP_NAME = 'select path,length from clips where name = ?'
DB_PATH = 'dankclips.db'
KODI_URL = 'http://localhost:7777/jsonrpc'
KODI_JSON = '{"jsonrpc": "2.0", "method": "Addons.ExecuteAddon","params": { "addonid": "script.clipplay", "params" : ["%s","%s"]}}'
PAGE = None
BUTTON_LINE = '<button type="submit" action="/start_clip" name="clip" value="%s"/>%s</button> ---- <i>%s</i><br>'
@app.route('/')
def start_page():
	global PAGE
	if PAGE is None:
		PAGE = build_page()
	return PAGE
@app.route('/start_clip')
def start_clip():
	clip_name = request.args['clip']
	con = sqlite3.connect(DB_PATH)
	print(clip_name)
	matches = []
	with con:
		cur = con.cursor()
		cur.execute(DB_MAP_NAME,(clip_name,))
		matches += cur.fetchall()
	try:
		r = requests.post(url=KODI_URL,data=KODI_JSON % (matches[0][0],str(matches[0][1])),headers={'content-type' : 'application/json'})
		r.raise_for_status()
	except requests.ConnectionError as err:
		pass #we dont care about connectione
	return 	redirect(url_for('start_page'))

@app.route('/dank_confirm')
def dank_confirm():
	return "<h1>Dankness!</h1>"

def build_page():
	print('building page...')
	con = sqlite3.connect(DB_PATH)
	clips = []
	with con:
		cur = con.cursor()
		cur.execute(DB_GET_CLIPS)
		clips += cur.fetchall()
	page = '<h1>Choose the dankest of memes!</h1><FORM action="/start_clip"><P>'
	for clip in clips:
		page += BUTTON_LINE % (clip)
	return page+"</P></FORM>"
