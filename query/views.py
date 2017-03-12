from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import requests

from .models import Query



def spotify_track_lookup(url):
	preview = ""
	song_request = requests.get(url)
	data = json.loads(song_request.text)
	if(len(data['tracks'].get(('items'))) == 0):
		return ""
	return str(data['tracks'].get('items')[0].get('external_urls'))[15:-2]

def get_query(chord_list):
	if(len(chord_list) < 2):
		return ""
	out = 'cp='
	for i in chord_list:
		if(i != '0'):
			out += (i + ',')
	return out[:-1]


def index(request):
	chords = []
	chords.append(request.GET.get('choiceOne'))
	chords.append(request.GET.get('choiceTwo'))
	chords.append(request.GET.get('choiceThree'))
	chords.append(request.GET.get('choiceFour'))
	hook_login = {
		"username": 'alexanderinsa',
		'password': 'css490cloud'
	}

	hook_login_request = requests.post(
		'https://api.hooktheory.com/v1/users/auth',
		data=hook_login
	)

	hook_auth_json = hook_login_request.json()

	id = hook_auth_json.get('id')
	username = hook_auth_json.get('username')
	activkey = hook_auth_json.get('activkey')


	hook_request_header = {
		'Authorization': 'Bearer ' + activkey,
	}

	query = get_query(chords)

	hook_song_request = requests.get(
		'https://api.hooktheory.com/v1/trends/songs?' + query,
		headers = hook_request_header,
	)

	track_urls = {}
	template = loader.get_template('query/index.html')
	context = {'track_urls': track_urls}
	
	if(hook_song_request.text == 'No songs match this chord progression'):
		return HttpResponse(template.render(context, request))


	d = json.loads(hook_song_request.text)

	song_list = {}
	for i in d:
		song_list[i['song']] = i['artist']


	for key, val in song_list.items():
		url = 'https://api.spotify.com/v1/search/?q='
		query = 'track:' + key.replace(" ", "+") + '+artist:' + val.replace(" ", "+") + '&type=track' 
		track_url = spotify_track_lookup(url + query)
		if(len(track_url) > 0):
			track_urls[key + ', ' + val] = (track_url)
		

	

	return HttpResponse(template.render(context, request))

# Create your views here.
