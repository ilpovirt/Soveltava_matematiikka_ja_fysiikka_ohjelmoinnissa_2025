import streamlit as st #asenna: pip install streamlit
#Ladataan data
import pandas as pd

df = pd.read_csv('./Data/GPS_data.csv')

#Annetaan visualisoinnille otsikko
st.title('GPS-havaintoja kuntopolulta')

#Kuvaajia voidaan piirtää Streamlitin omilla grafiikkatyökaluilla:

st.line_chart(df, x = 'Time (s)', y = 'Satellites', x_label = 'Time (s)', y_label = 'Satellites')
st.line_chart(df, x = 'Time (s)', y = 'Horizontal Accuracy (m)',x_label = 'Time (s)', y_label = 'Horizontal Accuracy (m)' )

#Myös Matplotlibin grafiikoita voi käyttää
# d) Laske kuljettu matka käyttäen Haversinen kaavaa.
#Lasketaan matka käyttäen Haversinen kaava
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

#Lasketaan kuljettu matka
import numpy as np
df['Distance_calc'] = np.zeros(len(df))

#lasketaan väimatka havaintopisteiden välillä käyttäen For-luuppia
for i in range(len(df)-1):
    lon1 = df['Longitude (°)'][i]
    lon2 = df['Longitude (°)'][i+1]
    lat1 = df['Latitude (°)'][i]
    lat2 = df['Latitude (°)'][i+1]
    df.loc[i+1,'Distance_calc'] = haversine(lon1, lat1, lon2, lat2)

#Lasketaan kokonaismatka mittapisteiden välisestä matkasta
df['total_distance'] = df['Distance_calc'].cumsum()
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,5))
plt.plot(df['Time (s)'],df['total_distance'])
plt.plot(df['Time (s)'],df['Distance (km)'])
plt.ylabel('Kokonaismatka')
plt.xlabel('Aika')
st.pyplot(fig)

#Kartta
import folium
from streamlit_folium import st_folium
#Määritellään "karttapohja", eli kartan keskipiste
lat1 = df['Latitude (°)'].mean() #Latitudin keskiarvo
long1 = df['Longitude (°)'].mean() #Longitudin keskiarvo

#luodaan kartta
my_map = folium.Map(location = [lat1,long1], zoom_start=15)

#Piirretään reitti kartalle:
folium.PolyLine(df[['Latitude (°)','Longitude (°)']], color = 'red', weight = 3).add_to(my_map)
st_map = st_folium(my_map, width = 900, height=650)