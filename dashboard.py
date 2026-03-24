
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")

@st.cache_data
def load_data():
    used_cols = [
        'FlightDate', 
        'Marketing_Airline_Network', 
        'OriginCityName', 
        'DestCityName', 
        'CarrierDelay', 
        'WeatherDelay', 
        'NASDelay', 
        'SecurityDelay', 
        'LateAircraftDelay'
    ]
    
    df = pd.read_parquet(
        "bts_delayed_flights_only_2018_2025.parquet", 
        engine='pyarrow',
        columns=used_cols
    )
    
    cat_cols = ['Marketing_Airline_Network', 'OriginCityName', 'DestCityName']
    df[cat_cols] = df[cat_cols].astype('category')
    
    causes = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    for col in causes:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['FlightDate'] = pd.to_datetime(df['FlightDate'])
    
    df['Year'] = df['FlightDate'].dt.year.astype('int16')
    df['Quarter'] = df['FlightDate'].dt.to_period('Q').astype(str).astype('category')
    df['Month'] = df['FlightDate'].dt.to_period('M').astype(str).astype('category')
    df['Week'] = df['FlightDate'].dt.to_period('W').astype(str).astype('category')
    
    return df

st.title("US Flight Delay Analysis (2018 - 2025)")

with st.spinner("Loading 10M+ rows into memory..."):
    df = load_data()

st.sidebar.header("Dashboard Controls")

min_date = df['FlightDate'].min()
max_date = df['FlightDate'].max()

date_range = st.sidebar.date_input(
    "Zoom in to Specific Time Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

agg_level = st.sidebar.selectbox(
    "Aggregate Results By",
    options=['Year', 'Quarter', 'Month', 'Week'],
    index=0
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df['FlightDate'] >= pd.to_datetime(start_date)) & (df['FlightDate'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]
else:
    filtered_df = df

st.header("1. Delays Over Time (All Years)")

# Changed from filtered_df to df to ignore the sidebar date filter
time_agg = df.groupby(agg_level).size().reset_index(name='Delay Count')
time_agg[agg_level] = time_agg[agg_level].astype(str) 

fig_time = px.line(
    time_agg, 
    x=agg_level, 
    y='Delay Count', 
    title=f"Total Delays Aggregated by {agg_level} (Global View)"
)
fig_time.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig_time, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.header("2. Breakdown by Carrier")
    carrier_agg = filtered_df['Marketing_Airline_Network'].value_counts().reset_index()
    carrier_agg.columns = ['Carrier', 'Delay Count']
    carrier_agg['Carrier'] = carrier_agg['Carrier'].astype(str) 
    
    fig_carrier = px.bar(carrier_agg.head(10), x='Carrier', y='Delay Count', title="Top 10 Carriers by Delays")
    fig_carrier.update_layout(yaxis_tickformat=',')
    st.plotly_chart(fig_carrier, use_container_width=True)

with col2:
    st.header("3. Breakdown by Cause")
    causes = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    cause_sums = filtered_df[causes].sum().reset_index()
    cause_sums.columns = ['Cause', 'Total Minutes']
    fig_cause = px.pie(cause_sums, names='Cause', values='Total Minutes', title="Total Delay Minutes by Cause")
    st.plotly_chart(fig_cause, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.header("4. Top Origin Cities")
    origin_agg = filtered_df['OriginCityName'].value_counts().reset_index()
    origin_agg.columns = ['City', 'Delay Count']
    fig_origin = px.bar(origin_agg.head(10), x='Delay Count', y='City', orientation='h', title="Top 10 Origin Cities for Delays")
    fig_origin.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_origin, use_container_width=True)

with col4:
    st.header("5. Top Destination Cities")
    dest_agg = filtered_df['DestCityName'].value_counts().reset_index()
    dest_agg.columns = ['City', 'Delay Count']
    fig_dest = px.bar(dest_agg.head(10), x='Delay Count', y='City', orientation='h', title="Top 10 Destination Cities for Delays")
    fig_dest.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_dest, use_container_width=True)