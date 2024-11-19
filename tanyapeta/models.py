from django.db import models

class Klorofil(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    chla = models.FloatField()

    def __str__(self):
        return f"Klorofil-a: {self.chla}, Lat: {self.latitude}, Lon: {self.longitude}"

class Spl(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    spl = models.FloatField()

    def __str__(self):
        return f"SPL: {self.spl}, Lat: {self.latitude}, Lon: {self.longitude}"
