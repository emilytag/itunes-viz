#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import xml.etree.ElementTree as ET
import operator
import numpy as np
import pandas as pd
import datetime

'''
u'Album', u'Album Artist', u'Album Rating', u'Album Rating Computed',
       u'All Items', u'Artist', u'Artwork Count', u'Audiobooks', u'BPM',
       u'Bit Rate', u'Clean', u'Comments', u'Compilation', u'Composer',
       u'Date Added', u'Date Modified', u'Disc Count', u'Disc Number',
       u'Distinguished Kind', u'Explicit', u'File Folder Count', u'File Type',
       u'Genre', u'Grouping', u'Has Video', u'Kind', u'Library Folder Count',
       u'Location', u'Master', u'Movies', u'Music', u'Name',
       u'Part Of Gapless Album', u'Persistent ID', u'Play Count', u'Play Date',
       u'Play Date UTC', u'Playlist ID', u'Playlist Items',
       u'Playlist Persistent ID', u'Podcast', u'Podcasts', u'Protected',
       u'Purchased', u'Purchased Music', u'Rating', u'Rating Computed',
       u'Release Date', u'Sample Rate', u'Size', u'Skip Count', u'Skip Date',
       u'Smart Criteria', u'Smart Info', u'Sort Album', u'Sort Album Artist',
       u'Sort Artist', u'Sort Composer', u'Sort Name', u'Start Time',
       u'Stop Time', u'TV Shows', u'Total Time', u'Track Count', u'Track ID',
       u'Track Number', u'Track Type', u'Unplayed', u'Visible',
       u'Volume Adjustment', u'Work', u'Year', u'iTunesU']
'''

#parses XML to return all songs
def preproc(root):
  all_songs = []
  for child in root.iter('dict'):
    song_data = {}
    for x in child:
      if x.tag == 'key':
        key = x.text
      else:
        song_data[key] = x.text
    all_songs.append(song_data)
  all_songs = [x for x in all_songs if x.get('Genre', None) != 'Podcast']
  return pd.DataFrame(all_songs[2:])

#filters null artists and exports to csv
def all_songs_to_csv(all_songs):
  not_nan = all_songs[pd.notnull(all_songs['Artist'])]
  not_nan.to_csv('songs.csv', encoding='utf-8')  

def all_artists_to_csv(all_songs):
  not_nan = all_songs[pd.notnull(all_songs['Artist'])]['Artist']
  not_nan.to_csv('artists.csv', encoding='utf-8')

def main():
  tree = ET.parse(sys.argv[1])
  root = tree.getroot()
  all_songs = preproc(root)
  all_songs_to_csv(all_songs)
  all_artists_to_csv(all_songs) 
main()
