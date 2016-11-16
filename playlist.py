#!/usr/bin/env python

import httplib2
import os
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

def create_playlist(title, description=''):
  playlists_insert_response = youtube.playlists().insert(
    part="snippet,status",
    body=dict(
      snippet=dict(
        title=title,
        description=description,
      ),
      status=dict(
        privacyStatus="public"
      )
    )
  ).execute()
  return playlists_insert_response["id"]

def add_video_to_playlist(videoID, playlistID):
  add_video_request=youtube.playlistItems().insert(
    part="snippet",
    body={
      'snippet': {
        'playlistId': playlistID,
        'resourceId': {
          'kind': 'youtube#video',
          'videoId': videoID
        }
        #'position': 0
      }
    }
  ).execute()

def search_videos(query, max_results=1):
  search_response = youtube.search().list(
    q=query,
    type="video",
    part="id,snippet",
    maxResults=max_results
  ).execute()
  videos = []
  channels = []
  playlists = []

  for search_result in search_response.get("items", []):
    videos.append({
      'title': search_result["snippet"]["title"],
      'id': search_result["id"]["videoId"],
    })

  return videos
