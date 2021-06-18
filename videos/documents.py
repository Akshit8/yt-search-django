from django_elasticsearch_dsl import Document, fields, Index
from .models import VideoModel

VIDEO_INDEX = Index('videos')


@VIDEO_INDEX.doc_type
class VideoDocument(Document):
    title = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )

    description = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )

    published_at = fields.TextField(
        fields={
            'raw':{
                'type': 'date',
            }
            
        }
    )

    thumbnail = fields.TextField(
        fields={
            'raw':{
                'type': 'keyword',
            }
            
        }
    )

    class Django(object):
        model = VideoModel