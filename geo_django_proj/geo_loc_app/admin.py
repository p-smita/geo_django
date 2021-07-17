from django.contrib import admin

from .models import StationModel, SpatialPoints, WeatherForecast, Coordinates

admin.site.register(StationModel)
admin.site.register(SpatialPoints)
admin.site.register(WeatherForecast)
admin.site.register(Coordinates)
