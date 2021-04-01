from django.db import models

class KakaoTextFile(models.Model):
    file = models.FileField(blank=False, null=False)
    description = models.CharField(max_length=255, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.file.name)