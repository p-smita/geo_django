# Python Imports
import requests
import json

# Django Imports
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Internal Imports
from .models import StationModel, SpatialPoints, WeatherForecast, Coordinates

GET_POINT_URL = "https://api.weather.gov/points/"


class HomeView(View):
    template_name = 'geo_loc/home.html'

    def get(self, request):
        weather_details = WeatherForecast.objects.all()
        loc_list = []
        for weather in weather_details:
            color = self.get_color(weather.temperature)
            coordinate_list = Coordinates.objects.filter(weather_forecast=weather)
            c_lst = []
            for c in coordinate_list:
                lst = [[float(c.latitude), float(c.longitude)]]
                c_lst.extend(lst)

            loc_list.append({
                "type": "Feature",
                "properties": {"color": color},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [c_lst]
                }
            })
        return render(request, self.template_name, {'loc_list': json.dumps(loc_list)})

    def get_color(self, temperature):
        if 96 <= temperature <= 99:
            color = 'green'
        elif temperature < 96:
            color = 'red'
        else:
            color = 'orange'
        return color


def load_spatial_data(request):
    json_file = open('spatial_data.json')
    json_data = json.load(json_file)
    for data in json_data:
        status = True if data.get('station_status') == 'Active' else False
        StationModel.objects.create(
            station_name=data.get('station_name'),
            latitude=data.get('location', {}).get('latitude'),
            longitude=data.get('location', {}).get('longitude'),
            status=status
        )
    return HttpResponse("Data uploaded")


def load_spatial_points(request):
    stations = StationModel.objects.filter(status=True)
    for station in stations:
        url = GET_POINT_URL + station.latitude + "," + station.longitude
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('properties', {})
            grid_x = data.get('gridX')
            grid_y = data.get('gridY')
            grid_id = data.get('gridId')
            forecast_url = data.get('forecast')
            SpatialPoints.objects.create(
                grid_x=grid_x, grid_y=grid_y, grid_id=grid_id,
                forecast_url=forecast_url
            )
    return HttpResponse("Spatial Points added")


class GetWeatherForecast(View):

    def get(self, request):
        spatial_points = SpatialPoints.objects.all()
        for spatial_pt in spatial_points:
            try:
                url = spatial_pt.forecast_url
                response = requests.get(url)
                if response.status_code == 200:
                    resp_data = response.json()
                    properties_data = resp_data.get('properties')
                    forecast_data = self.get_weather_details(properties_data)
                    forecast_obj = WeatherForecast.objects.create(**forecast_data)
                    geometry_data = resp_data.get('geometry')
                    self.save_coordinates(geometry_data, forecast_obj)
            except:
                continue
        return HttpResponse("Data collected successfully")

    def get_weather_details(self, data):
        for period in data.get('periods'):
            if period.get('number') == 1:
                split_wind_speed = period.get('windSpeed').split('to')
                min_speed = split_wind_speed[0].strip()
                max_speed_split = split_wind_speed[1].strip().split(" ")
                max_speed = max_speed_split[0]
                speed_unit = max_speed_split[1]
                forecast_data = {
                    'name': period.get('name'),
                    'start_time': period.get('startTime'),
                    'end_time': period.get('endTime'),
                    'temperature': period.get('temperature'),
                    'temperature_unit': period.get('temperatureUnit'),
                    'min_wind_speed': float(min_speed),
                    'max_wind_speed': float(max_speed),
                    'wind_speed_unit': speed_unit,
                    'icon_url': period.get('icon'),
                    'short_description': period.get('shortForecast'),
                    'details': period.get('detailedForecast')
                }
                return forecast_data

    def save_coordinates(self, geometry_data, forecast_obj):
        coordinates = geometry_data.get('coordinates')[0]
        for coordinate in coordinates:
            try:
                Coordinates.objects.create(
                    weather_forecast=forecast_obj,
                    latitude=coordinate[0],
                    longitude=coordinate[1]
                )
            except:
                continue