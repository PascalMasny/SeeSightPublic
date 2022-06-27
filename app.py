import streamlit as st
from PIL import Image

from WeatherApi import weather_api
from RouteApi import routegen

import pandas as pd
import numpy as np

#! Page Settings
st.set_page_config(layout="wide",
    page_icon="✈️", 
    page_title="SeeSight")
#? Header
st.header('Seesight')


#? Weather
#Data and Input => https://docs.streamlit.io/library/api-reference/data/st.metric
city_name = st.text_input('City Name', 'Augsburg')
str_show = "The Weather in " + city_name + " is:"
st.write(str_show)

#Data API
temperature, humidity, pressure, description = weather_api.get_weather(city_name)
temperature = weather_api.kelvinToCelsius(temperature)
temperature = str('%.5s' % temperature) + " °C"
humidity = str(humidity) + "  %"
pressure = str(pressure) + " hPa"
description = str(description)

#Data Emoji
description_name = ["clear sky", "few clouds", "scattered clouds", "broken clouds", "shower rain", "rain", "thunderstorm", "snow", "mist"]
description_emoji = ["☀️", "☁️☀️", "☁️" , "☁️🌧️", "🌧️☁️", "☁️🌧️", "🌧️", "⛈️", "❄️", "🌫️"]

#Data Visualation 
col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", temperature)
col2.metric("Humidity", humidity)
col3.metric("Humidity", pressure)
col4.metric("Description", description)


#? sep line
st.markdown("""---""")


#?Route Gen
#Points
start = st.text_input('Start Point', 'Königsplatz Augsburg')
finish = st.text_input('Finish Point', 'Clever Fit Lechhausen')
waypoints = ["Fuggerei", 
"Rathaus Augsburg", 
"Citygalerie Augsburg"]

#select otions
options = st.multiselect("Select your waypoints", waypoints)
option_mode = st.selectbox('Select transportation mode',('walking', 'driving', 'bicycling', 'transit'))


#generate route
route_df = routegen.gen_route_df(start, finish, options)

#calc distance
distance_df = routegen.calc_distance(route_df)


#? sep line
st.markdown("""---""")


#? show data 
col1, col2 = st.columns(2)

with col1:
    zoom  = st.slider('Map zoom', 6, 26, 13)
    option_maptype = st.selectbox('Select your maptype',("roadmap", "satellite", "hybrid", "terrain"))

    #gen picture
    routegen.gen_maps_png(route_df, options, option_mode, option_maptype, zoom)
    image = Image.open('img/route.jpg')
    st.image(image)

with col2:
    st.table(distance_df)