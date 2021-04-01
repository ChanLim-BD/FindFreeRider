from .models import KakaoTextFile
from rest_framework import serializers


class TextFileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta():
        model = KakaoTextFile
        fields = ('file', 'description', 'uploaded_at')