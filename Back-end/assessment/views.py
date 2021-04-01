from django.http import JsonResponse, HttpResponse

from dataAnalysis import DataAnalasis

from assessment.models import KakaoTextFile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from assessment.serializers import TextFileSerializer


class TextFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = TextFileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            filename = serializer.data['file']
            DA = DataAnalasis(filename)
            response = DA.runModule()

            return HttpResponse(response)
        else:
            return Response(serializer.errors)
