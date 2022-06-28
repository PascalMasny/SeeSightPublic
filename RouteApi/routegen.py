
import pandas as pd
from geopy.geocoders import GoogleV3
import geopy.distance
import geopy
import googlemaps
from datetime import datetime, timedelta
import array
import streamlit as st


#? API
API = st.secrets["maps"]
gmaps = googlemaps.Client(key=API)
gmap = googlemaps.Client(key=API)
geolocator = GoogleV3(api_key=API)
#print(type(geolocator))
#print(type(gmap))
#print(type(gmaps))



def gen_route_df(start, finish, waypoints):

    waypoints.insert(0, start)
    waypoints.append(finish)

    #print(waypoints)

    #init df
    df_location = pd.DataFrame(columns=['name', 'address', 'lat', 'lon'])

    for name in waypoints:
        #print(name)

        location = geolocator.geocode(name)


        #print(location.address)
        #print(location.latitude, location.longitude)

        df_tmp = pd.DataFrame([[name, location.address, location.latitude, location.longitude]],
                columns=['name', 'address', 'lat', 'lon'])

        df_location = pd.concat([df_location, df_tmp], ignore_index=True)

        #print(df_tmp)
        #print("\n")


    #print(df_location)
    return df_location


def calc_distance(df_location):

    df_len = len(df_location)
    df_distance = pd.DataFrame(columns=['from', 'to', 'distance'])

    for column in range(df_len):
        try:
            #print(column)
        
            p1 = df_location['lat'][column], df_location['lon'][column]
            p2 = df_location['lat'][column+1], df_location['lon'][column+1]

            d_goog = gmap.distance_matrix(p1, p2, mode='driving')
            #print(d_goog)
            d = d_goog['rows'][0]['elements'][0]['distance']['value']
            d = d / 1000 #meters to km
            #print(d)

            df_tmp = pd.DataFrame([[df_location['name'][column], df_location['name'][column+1], d]],
                    columns=['from', 'to', 'distance'])

            df_distance = pd.concat([df_distance, df_tmp], ignore_index=True)
        except:
            print("")

    #print(df_distance)
    return df_distance


def gen_maps_png(df_location, waypoints, mode, maptype, zoom):

    start = df_location['name'][0]
    finish = df_location['name'][int(str(len(df_location) - 1))]
    #print(start, finish)

    waypoints = waypoints
    #print(waypoints)

    # https://developers.google.com/maps/documentation/directions/get-directions#TravelModes
    results = gmaps.directions( origin = start,
                            destination = finish,                                     
                            waypoints = waypoints,
                            optimize_waypoints = True,
                            mode = mode) #driving, walking, bicycling, transit (bus, subway, train, tram, rai,m trennbar mit | [https://developers.google.com/maps/documentation/directions/get-directions#transit_mode])
                            #departure_time=datetime.now()+ timedelta(hours=1))
    #print(results)

    marker_points = []
    waypoints = []

    for leg in results[0]["legs"]:
        leg_start_loc = leg["start_location"]
        marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
        for step in leg["steps"]:
            end_loc = step["end_location"]
            waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')

    last_stop = results[0]["legs"][-1]["end_location"]
    marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

    #? set marker coulor
    markers = [ "color:blue|size:mid|label:" + chr(65+i) + "|" 
            + r for i, r in enumerate(marker_points)]

    #? set picture
    result_map = gmaps.static_map(
                    center = waypoints[0],
                    scale=2, 
                    zoom=zoom,
                    size=[1000, 1000], 
                    format="jpg", 
                    maptype= maptype, #roadmap, satellite, hybrid, terrain
                    markers=markers,
                    path="color:0x0000ff|weight:2|" + "|".join(waypoints))

    #? save picture
    with open("img/route.jpg", "wb") as img:
        for chunk in result_map:
            img.write(chunk)
