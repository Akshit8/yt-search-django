from django_elasticsearch_dsl import fields
from .models import VideoModel
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import VideoDocument

class VideoDocumentSerializer(DocumentSerializer):
    class Meta(object):
        model = VideoModel
        document = VideoDocument

        fields = ('id', 'title', 'description', 'published_at', 'thumbnail')

