from django.db import models

class City(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name