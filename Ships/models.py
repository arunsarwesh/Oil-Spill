from django.db import models

class PositionReport(models.Model):
    ship_id = models.BigIntegerField()  # Ship identifier (UserID from AIS data)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Latitude with precision
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Longitude with precision
    name = models.CharField(max_length=255, default='NIL')  # Optional name, default to 'NIL'
    speed = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Speed (SOG) in knots, default to 0
    Cog = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Allow null values   
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp when the record is created

    class Meta:
        verbose_name = 'Position Report'
        verbose_name_plural = 'Position Reports'
        indexes = [
            models.Index(fields=['ship_id']),  # Index for ship ID to improve query performance
        ]
#
    def __str__(self):
        return f"Ship ID: {self.ship_id} | Lat: {self.latitude}, Lon: {self.longitude} | Time: {self.timestamp}"
