from django.db import models


class StationModel(models.Model):
    """
    Model to store stations
    """
    station_name = models.CharField(max_length=150)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)
    status = models.BooleanField(default=True)


class SpatialPoints(models.Model):
    """
    Model to store spatial points required for getting weather forecast
    """
    forecast_url = models.CharField(max_length=200)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    grid_id = models.CharField(max_length=10)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class WeatherForecast(models.Model):
    """
    Model to store weather forecast details
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    temperature = models.FloatField()
    temperature_unit = models.CharField(max_length=5)
    min_wind_speed = models.FloatField()
    max_wind_speed = models.FloatField()
    wind_speed_unit = models.CharField(max_length=5)
    icon_url = models.URLField()
    short_description = models.CharField(max_length=256, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Coordinates(models.Model):
    """
    Model to store forecast coordinates
    """
    weather_forecast = models.ForeignKey(WeatherForecast, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=25)
    longitude = models.CharField(max_length=25)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)