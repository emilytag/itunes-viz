#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import json 

base_url = "http://api.genius.com"
search_url = base_url + "/search"

with open('artists_seen.json') as seen:
  try:
    artist_seen = json.loads(seen)
  except:
    artist_seen = {}
with open('artist2lyricsmap.json') as lyricsmap:
  try:
    all_lyrics = json.loads(lyricsmap)
  except:
    all_lyrics = {}

access_token = '??????'
headers = {'Authorization': 'Bearer '+access_token}

#from tutorial https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/ huge help
#gets song url from api and parses for lyrics using beautifulsoup
def getLyrics(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]
  page_url = "http://genius.com" + path

  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  [h.extract() for h in html('script')]
  lyrics = html.find('div', class_='lyrics').get_text()

  print lyrics
  return lyrics

#gets artist api path
def getArtist(song_api_path, artist_name):
  song_url =  base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  artist = json["response"]["song"]["primary_artist"]

  if artist["name"].lower() == artist_name:  
    return artist["api_path"]
  else:
    return None

#gets api paths for all songs of an artist
def getSongPaths(artist_api_path):
  api_paths = []
  artist_url = base_url + artist_api_path + "/songs"
  data = {"per_page": 50}
  all_songs = True

  while all_songs:
    response = requests.get(artist_url, data=data, headers=headers)
    json = response.json()
    songs = json["response"]["songs"]
    for song in songs:
      api_paths.append(song["api_path"])
      if len(songs) < 50:
        all_songs = False
      else:
        if "page" in data:
          data["page"] = data["page"] + 1
        else:
          data["page"] = 1

  return list(set(api_paths))

#gets json dump for song api point
def getSongInfo(song_api_path):
  song_url =  base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  return json

if __name__ == "__main__":
  with open(sys.argv[1]) as songs:
    lines = songs.readlines()[1:] #skips header
    for line in lines:
        line_split = line.split("\t")
        song_title = line_split[34].lower()
        artist_name = line_split[6].lower().replace(",", "")

        #checks if artist and song are done
        artist_done = all_lyrics.get(artist_name, None)
        song_done = None
        song_info = None
        if artist_done:
          song_done = all_lyrics[artist_name].get(song_title, None)

        #otherwise do the thing
        if not song_done:
          print "getting lyrics for...{} - {}".format(artist_name, song_title)
          params = {'q': song_title}
          response = requests.get(search_url, params=params, headers=headers)
          json = response.json()

          #break if found by searching by song title
          for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"].lower() == artist_name:
              song_info = hit
              break

          #else search by artist
          if not song_info:
            print("searching by artist.....")
            artist_api_path = artist_seen.get(artist_name, None)
            
            #check pickled dict of { artist name -> api path } to save from looking it up again
            if not artist_api_path: 
              params = {'q': artist_name}
              response = requests.get(search_url, params=params, headers=headers)
              artist_info = response.json()
              for hit in artist_info["response"]["hits"]:
                song_api_path = hit["result"]["api_path"]
                artist_api_path = getArtist(song_api_path, artist_name)
                if artist_api_path:
                  artist_seen[artist_name] = artist_api_path
                  break

            #look for the song based on the artist api path
            if artist_api_path and artist_api_path != "Not Found":
              song_api_paths = getSongPaths(artist_api_path) 
              for song_api_path in song_api_paths:
                api_id = song_api_path.split('/')[2]
                full_song_info = getSongInfo(song_api_path)
                info_title = full_song_info["response"]["song"]["title"]
                if info_title.lower() == song_title:
                  song_info = full_song_info
                  break
            else:
              artist_seen[artist_name] = "Not Found"
          
          #if found through song or artist get the lyrics from beautifulsoup and serialize
          if song_info:
            try:
              song_api_path = song_info["result"]["api_path"]
            except KeyError:
              song_api_path = song_info["response"]["song"]["api_path"]
            lyrics = getLyrics(song_api_path)
            if artist_name in all_lyrics:
              all_lyrics[artist_name][song_title] = lyrics
            else:
              all_lyrics[artist_name] = {song_title: lyrics}
            with open('artists_seen.json', 'w') as seen:
                json.dumps(artist_seen, seen, ensure_ascii=False)
            with open('artist2lyricsmap.json', 'w') as lyricsmap:
                json.dumps(all_lyrics, lyricsmap, ensure_ascii=False)
          
          else:
            print("***CANT FIND***")
            try:
              all_lyrics[artist_name][song_title] = "Not Found"
            except:
              all_lyrics[artist_name] = {song_title: "Not Found"}
