import sched
import time
import os
from datetime import datetime, timezone, timedelta

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from elastic import getElasticClient, indexVideo

# youtube api config
DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# some random queries for youtube api
queries = [
    'blockchain',
    'business insider',
    'react js tutorial',
    'top 10 expensive watches',
    'top 10 alt coins'
]

# defines client for Youtube API
def getClient():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    return youtube

# gets video from youtube API and indexes them to elastic search
def searchVideosAndIndex(es, query, limit):
    youtube = getClient()

    # searches all videos published in last 24hrs.
    # To avoid collision 100% i.e no same video is retrieved, retrieve the timestamp of latest
    # video from elastic search and use it.
    published_after = (datetime.now(timezone.utc) - timedelta(days=1)).astimezone().isoformat()

    response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=limit,
        publishedAfter=published_after
    ).execute()

    for video in response['items']:
        video = {
            'id' : video['id']['videoId'],
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'published_at': video['snippet']['publishTime'],
            'thumbnail': video['snippet']['thumbnails']['default']['url']
        }

        indexVideo(es, video)
    

if __name__ == '__main__':
    try:
        print("starting yt worker")

        es = getElasticClient()
        if es == None:
            raise Exception("unable to connect to elastic search")
        else:
            print("sucessfully connected to elastic search")
        
        s = sched.scheduler(time.time, time.sleep)
        
        def startWorker(sc):
            try:
                for q in queries:
                    print(q)
                    searchVideosAndIndex(es, q, 5)
                    s.enter(24 * 60 * 60, 1, startWorker, (sc, ))
            except HttpError as err:
                print(err)
                exit()

        s.enter(10, 1, startWorker, (s,))
        s.run()
    except Exception as ex:
        print(ex)
        exit()