# Django Imports
from django.urls import path

# Internal Imports
from .views import HomeView, load_spatial_data, load_spatial_points, GetWeatherForecast


urlpatterns = [
    path('', HomeView.as_view(), name='home-page'),
    path('get_forecast', GetWeatherForecast.as_view(), name='get-forecast'),
    path('load_spatial_data', load_spatial_data, name='load-spatial-data'),
    path('load_spatial_points', load_spatial_points, name='load-spatial-points'),
]
