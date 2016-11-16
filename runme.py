#!/usr/bin/env python
from playlist import create_playlist, add_video_to_playlist, search_videos

with open('songs.txt') as f:
    playlist_id = create_playlist('Songs that start with a J')
    for line in f:
       video = search_videos(line.rstrip())[0]
       print('Adding "{}"...'.format(video['title']))
       add_video_to_playlist(video['id'], playlist_id)
