from rest_framework import pagination
from .models import VideoModel
from .documents import VideoDocument
from .serializers import VideoDocumentSerializer

from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    SearchFilterBackend,
    OrderingFilterBackend
)

class VideoDocumentView(DocumentViewSet):
    document = VideoDocument
    serializer_class = VideoDocumentSerializer

    pagination_class = LimitOffsetPagination

    filter_backends = [
        SearchFilterBackend,
        OrderingFilterBackend
    ]

    search_fields = ('title', 'description')
    # multi_match_search_fields = ('title', 'description')
    # filter_fields = {
    #     'title' : 'title',
    #     'description' : 'description',
    # }

    ordering_fields = {
        'published_at': None
    }
    ordering = ('published_at',)