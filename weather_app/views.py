from django.shortcuts import render
import json
import requests
import datetime
import geocoder
from . import location
from . import direction
from . import timing
from . import air_quality

aqi_dic={1:'Good', 2:'Fair', 3:'Moderate', 4:'Poor', 5:'Very Poor'}

def index(request):
    api_key = 'a928ada05edaba3600047c97b1f326c8'
    search_url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'
    aqi_url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']


        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url, aqi_url)

    
        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,

        }

        return render(request, 'weather_app/index.html', context)
    else:
        lat, lon=location.user()
        weather_data1, daily_forecasts1 = auto(lat, lon, api_key, search_url, forecast_url, aqi_url)
        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
        }
        return render(request, 'weather_app/index.html', context)


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url, aqi_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    pop=int((forecast_response['daily'][0]['pop'])*100)

    aqi_response = requests.get(aqi_url.format(lat, lon, api_key)).json()

    aqi_main=aqi_response['list'][0]['main']['aqi']
    aqi=aqi_dic[aqi_main]

    sunrise=datetime.datetime.utcfromtimestamp(int(response['sys']['sunrise'])+int(response['timezone'])).strftime('%H:%M')
    sunset=datetime.datetime.utcfromtimestamp(int(response['sys']['sunset'])+int(response['timezone'])).strftime('%H:%M')
    time=timing.current_time(response['timezone']).strftime('%H:%M')
    tod=''
    if int(time[0:2])<int(sunrise[0:2]):
        tod='early'
    elif int(time[0:2]) in range(11,16):
        tod='midday'
    elif int(time[0:2]) in range(int(sunrise[0:2]), 12):
        tod='morning'
    elif int(time[0:2]) in range(16, int(sunset[0:2])+1):
        tod='evening'
    elif int(time[0:2])>int(sunset[0:2]):
        tod='night'


    def particulates(arg):
        return aqi_response['list'][0]['components'][arg]
    co=particulates('co')
    no=particulates('no')
    no2=particulates('no2')
    o3=particulates('o3')
    so2=particulates('so2')
    pm2_5=particulates('pm2_5')
    pm10=particulates('pm10')
    nh3=particulates('nh3')


    weather_data = {
        'city': response['name'],
        'temperature': round(response['main']['temp'] - 273.15, 1),
        'feels': round(response['main']['feels_like'] - 273.15, 1),
        'sunrise': datetime.datetime.utcfromtimestamp(int(response['sys']['sunrise'])+int(response['timezone'])).strftime('%I:%M %p'),
        'sunset': datetime.datetime.utcfromtimestamp(int(response['sys']['sunset'])+int(response['timezone'])).strftime('%I:%M %p'),
        'description': (response['weather'][0]['description']).title(),
        'visibility': int(response['visibility'])/1000,
        'humidity': response['main']['humidity'],
        'pressure': response['main']['pressure'],
        'wind': response['wind']['speed'],
        'direction': direction.dir(int(response['wind']['deg'])),
        'icon': response['weather'][0]['icon'],
        'lat': float(response['coord']['lat']),
        'lon': float(response['coord']['lon']),
        'prep': pop,
        'aqi_main': int(aqi_main)*100,
        'aqi': aqi,
        'time': timing.current_time(response['timezone']).strftime('%I:%M %p'),
        'tod': tod,
        'co': co,
        'no': no,
        'no2': no2,
        'o3': o3,
        'so2': so2,
        'pm2_5': pm2_5,
        'pm10': pm10,
        'nh3': nh3,
        'co_col': air_quality.co_col(int(co)),
        'o3_col': air_quality.o3_col(int(o3)),
        'pm2_5_col': air_quality.pm2_5_col(int(pm2_5)),
        'pm10_col': air_quality.pm10_col(int(pm10)),
        'no2_col': air_quality.no2_col(int(no2)),
        'so2_col': air_quality.so2_col(int(so2)),
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][1:8]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 1),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 1),
            'description': (daily_data['weather'][0]['description']).title(),
            'icon': daily_data['weather'][0]['icon'],
            'pop': float(daily_data['pop'])*100
        })

    return weather_data, daily_forecasts


def auto(lat, lon, api_key, search_url, forecast_url, aqi_url):
    response = requests.get(search_url.format(lat, lon, api_key)).json()
    
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    aqi_response = requests.get(aqi_url.format(lat, lon, api_key)).json()

    aqi_main=aqi_response['list'][0]['main']['aqi']
    aqi=aqi_dic[aqi_main]

    sunrise=datetime.datetime.utcfromtimestamp(int(response['sys']['sunrise'])+int(response['timezone'])).strftime('%H:%M')
    sunset=datetime.datetime.utcfromtimestamp(int(response['sys']['sunset'])+int(response['timezone'])).strftime('%H:%M')
    time=timing.current_time(response['timezone']).strftime('%H:%M')
    tod=''
    if int(time[0:2])<int(sunrise[0:2]):
        tod='early'
    elif int(time[0:2]) in range(11,16):
        tod='midday'
    elif int(time[0:2]) in range(int(sunrise[0:2]), 12):
        tod='morning'
    elif int(time[0:2]) in range(16, int(sunset[0:2])+1):
        tod='evening'
    elif int(time[0:2])>int(sunset[0:2]):
        tod='night'

    def particulates(arg):
        return aqi_response['list'][0]['components'][arg]
    co=particulates('co')
    no=particulates('no')
    no2=particulates('no2')
    o3=particulates('o3')
    so2=particulates('so2')
    pm2_5=particulates('pm2_5')
    pm10=particulates('pm10')
    nh3=particulates('nh3')


    pop=int((forecast_response['daily'][0]['pop'])*100)

    weather_data = {
        'city': response['name']+' (auto-detected)',
        'temperature': round(response['main']['temp'] - 273.15, 1),
        'feels': round(response['main']['feels_like'] - 273.15, 1),
        'sunrise': datetime.datetime.utcfromtimestamp(int(response['sys']['sunrise'])+int(response['timezone'])).strftime('%I:%M %p'),
        'sunset': datetime.datetime.utcfromtimestamp(int(response['sys']['sunset'])+int(response['timezone'])).strftime('%I:%M %p'),
        'description': (response['weather'][0]['description']).title(),
        'visibility': int(response['visibility'])/1000,
        'humidity': response['main']['humidity'],
        'pressure': response['main']['pressure'],
        'wind': response['wind']['speed'],
        'direction': direction.dir(int(response['wind']['deg'])),
        'icon': response['weather'][0]['icon'],
        'lat': float(response['coord']['lat']),
        'lon': float(response['coord']['lon']),
        'prep': pop,
        'aqi_main': int(aqi_main)*100,
        'aqi': aqi,
        'time': timing.current_time(response['timezone']).strftime('%I:%M %p'),
        'tod': tod,
        'co': co,
        'no': no,
        'no2': no2,
        'o3': o3,
        'so2': so2,
        'pm2_5': pm2_5,
        'pm10': pm10,
        'nh3': nh3,
        'co_col': air_quality.co_col(int(co)),
        'o3_col': air_quality.o3_col(int(o3)),
        'pm2_5_col': air_quality.pm2_5_col(int(pm2_5)),
        'pm10_col': air_quality.pm10_col(int(pm10)),
        'no2_col': air_quality.no2_col(int(no2)),
        'so2_col': air_quality.so2_col(int(so2)),
    }
    

    daily_forecasts = []
    for daily_data in forecast_response['daily'][1:8]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 1),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 1),
            'description': (daily_data['weather'][0]['description']).title(),
            'icon': daily_data['weather'][0]['icon'],
            'pop': float(daily_data['pop'])*100
            
        })

        


    return weather_data, daily_forecasts

    datetime.utcfromtimestamp(int(response['sys']['sunrise'])+int(response['timezone'])).strftime('%Y-%m-%d %H:%M:%S')


from django.shortcuts import render

def custom_500(request):
    return render(request, '500.html', status=500)