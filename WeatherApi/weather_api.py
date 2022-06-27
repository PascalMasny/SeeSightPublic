import requests
import json
import datetime
import streamlit as st


#API Key
api_key = st.secrets["weather"]
#base_url
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather(city_name):  

    #city name
    city_name =  "Augsburg"

    #complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    
    #Prit Data
    if x["cod"] != "404":

            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            print(" Temperature (in kelvin unit) = " +
                                            str(current_temperature) +
                    "\n atmospheric pressure (in hPa unit) = " +
                                            str(current_pressure) +
                    "\n humidity (in percentage) = " +
                                            str(current_humidity) +
                    "\n description = " +
                                            str(weather_description))

    else:
            print(" City 404 du kek! \n Denn sie existiert nicht \n HUAN!")


    #Print all the Data on more Time
    #print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_temperature, current_pressure, current_humidity)
    
    return current_temperature, current_humidity, current_pressure, weather_description

def kelvinToCelsius(kelvin):
    return kelvin - 273.15