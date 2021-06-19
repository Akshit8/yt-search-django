import os

from elasticsearch import Elasticsearch

# elastic configs
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT')
VIDEO_INDEX = os.environ.get('ELASTICSEARCH_INDEX')

# return singleton elastic-client
def getElasticClient():
    es = Elasticsearch([{
        'host': ELASTICSEARCH_HOST,
        'port': ELASTICSEARCH_PORT
    }])
    if es.ping():
        return es
    
    return None

# indexes given video in elastic-search
# replace this query with bulk indexing
def indexVideo(es: Elasticsearch, body):
    try:
        # will autocreate the index if not exists.
        es.index(
            index=VIDEO_INDEX,
            doc_type='_doc',
            body=body
        )
        print("video indexed sucessfully")
    except Exception as ex:
        # not exitting for exception
        print(ex)