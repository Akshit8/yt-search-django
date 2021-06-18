import sched
import time
import os

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

    response = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=limit
    ).execute()

    for video in response['items']:
        id = video['id']['videoId']

        video = {
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'published_at': video['snippet']['publishTime'],
            'thumbnail': video['snippet']['thumbnails']['default']['url']
        }

        indexVideo(
            es,
            id,
            video
        )
    


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

        s.enter(2, 1, startWorker, (s,))
        s.run()
    except Exception as ex:
        print(ex)
        exit()