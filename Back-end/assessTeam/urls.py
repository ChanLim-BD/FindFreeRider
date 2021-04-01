from django.conf.urls import url
from assessment.views import TextFileView

urlpatterns = [
    url(r'^upload/$', TextFileView.as_view(), name='file-upload'),
]
