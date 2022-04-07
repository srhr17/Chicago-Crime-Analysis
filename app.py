import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL=("Crimes_-_2001_to_Present.csv")

st.set_page_config(
        page_title="Crime Analysis in Chicago",
        page_icon="chi.jpg",
        layout="wide",
    )
# st.title("Crime Analysis in Chicago")	
st.markdown("<h1 style='text-align: center; color: white;letter-spacing:2px;'>Crime Analysis in Chicago</h1>", unsafe_allow_html=True)
st.markdown(" <h5 style='text-align: center;font-weight: normal;letter-spacing:5px; color: white;'>This app is a Streamlit dashboard that can be used to analyze crimes in Chicago</h5>", unsafe_allow_html=True)

@st.cache(persist=True)
def loadData(row_limit):
    df = pd.read_csv(DATA_URL,nrows=row_limit,parse_dates=['Date'])
    df.drop(columns=['ID','Description','FBI Code','X Coordinate','Y Coordinate','Year','Updated On','Location'],inplace=True)
    df.dropna(subset=['Latitude','Longitude'],inplace=True)
    df.rename(lambda x: str(x).lower(),axis='columns',inplace=True)
    return df

def insertSpace():
    st.text("")
    st.markdown("***")
    st.text("")
data_frame = loadData(100000)

# st.write(data_frame.columns)

# st.header("Number of People injured in Collisions")
# injured_people = st.slider("Number of People injured in Collisions",0,19)
# st.map(data_frame.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))

# st.header("Number of People injured by hour of the day")
# hour = st.sidebar.slider("Hour of the day",0,23)
# st.map(data_frame[data_frame["crash_date_crash_time"].dt.hour==hour][["latitude","longitude"]].dropna(how="any"))

# st.header("Vehicle collision between %i and %i hours" % (hour,hour+1))
# st.write(pdk.Deck(
#     map_style="mapbox://styles/mapbox/light-v9",
#     initial_view_state={
#      "latitude":data_frame["latitude"].mean(),
#     "longitude":data_frame["longitude"].mean(),
#     "zoom":11,
#     "pitch":50
#     },
#       layers=[pdk.Layer("HexagonLayer",
#                         data=data_frame[['crash_date_crash_time','latitude','longitude']],
#                         get_position=['longitude','latitude'],
#                         radius=100,
#                         extruded=True,
#                         pickable=True,
#                         elevation_scale=4,
#                         elevation_range=[0,1000]  )]
# ))

# st.subheader("Breakdown by minutes between %i and %i hours" % (hour,hour+1))
# filtered=data_frame[(data_frame['crash_date_crash_time'].dt.hour>=hour) & (data_frame['crash_date_crash_time'].dt.hour<hour+1)]
# hist=np.histogram(filtered['crash_date_crash_time'].dt.minute,bins=60,range=(0,60))[0]
# chart_data = pd.DataFrame({"minute":range(60),"crashes":hist})
# fig = px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
# st.write(fig)

insertSpace()
# st.header("Area by Crime Type")
st.markdown("<h2 style='text-align: center; color: white;'>Locations and summary by Crime Type</h2>", unsafe_allow_html=True)
select = st.selectbox('Crime Types ',['ARSON', 'ASSAULT', 'BATTERY', 'BURGLARY', 'CONCEALED CARRY LICENSE VIOLATION', 'CRIM SEXUAL ASSAULT', 'CRIMINAL DAMAGE', 'CRIMINAL SEXUAL ASSAULT', 'CRIMINAL TRESPASS', 'DECEPTIVE PRACTICE', 'GAMBLING', 'HOMICIDE', 'HUMAN TRAFFICKING', 'INTERFERENCE WITH PUBLIC OFFICER', 'INTIMIDATION', 'KIDNAPPING', 'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT', 'NARCOTICS', 'NON - CRIMINAL', 'NON-CRIMINAL', 'OBSCENITY', 'OFFENSE INVOLVING CHILDREN', 'OTHER NARCOTIC VIOLATION', 'OTHER OFFENSE', 'PROSTITUTION', 'PUBLIC INDECENCY','PUBLIC PEACE VIOLATION', 'ROBBERY', 'SEX OFFENSE', 'STALKING', 'THEFT', 'WEAPONS VIOLATION'])
subsetted_data = data_frame[data_frame['primary type']==select]
st.markdown('**Number of Crimes:** %i' % subsetted_data.shape[0])
st.markdown('**Arrests:** %i' % subsetted_data['arrest'].sum())
st.table(subsetted_data['location description'].value_counts().head(10))
st.map(subsetted_data[['latitude','longitude']].dropna(how="any"))
st.subheader("Check the box to see the data by crime type")    
if st.checkbox('Show Data by Crime Type',False):
    st.write(subsetted_data.dropna(how="any"))
insertSpace()
st.subheader("Check the box to see/play with raw data")    
if st.checkbox('Show Raw Data',False):
    st.write(data_frame)