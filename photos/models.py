from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=255)
    albumId = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    dominant_color = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.width}x{self.height}/{self.dominant_color}"