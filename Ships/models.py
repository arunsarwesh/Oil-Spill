# In Ships/models.py

from django.db import models

class PositionReport(models.Model):
    ship_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255, default='NIL')
    cargo_type = models.CharField(max_length=255, default='NIL')
    speed = models.FloatField(default=0.0)  # Add this line for speed

    timestamp = models.DateTimeField(auto_now_add=True)  # Assuming you have a timestamp field
