import pandas as pd
# Stops for 20 secs at each station
# time = next stop arrival_id - previous stop departure_id 
# distance = next stop_id -  previous stop_id
st = pd.read_csv('Dataset/stop_time2.txt')


def process_trip(trip_df):
    
    # Sort by stop_sequence
    trip_df = trip_df.sort_values(by='stop_sequence')
    trip_df['point_distance'] = trip_df['shape_dist_traveled'].diff().fillna(0)
    # print(trip_df[['trip_id','stop_id','stop_sequence','point_distance']])
    trip_df['arrival_time'] = pd.to_timedelta(trip_df['arrival_time'])
    trip_df['departure_time'] = pd.to_timedelta(trip_df['departure_time'])
    trip_df['individual_time'] = (trip_df['arrival_time'] - trip_df['departure_time'].shift()).fillna(pd.Timedelta(seconds=0))

    trip_df['arrival_time'] = trip_df['arrival_time'].apply(lambda x: str(x).replace('0 days ', ''))
    trip_df['departure_time'] = trip_df['departure_time'].apply(lambda x: str(x).replace('0 days ', ''))    
    trip_df['individual_time'] = trip_df['individual_time'].apply(lambda x: str(x).replace('0 days ', ''))
    trip_df['individual_time'] = trip_df['individual_time'].apply(lambda x: str(x).replace('-1 days ', ''))
    return trip_df


processed_trip_df = st.groupby('trip_id').apply(process_trip).reset_index(drop=True)

# Display the processed DataFrame
print(processed_trip_df[['trip_id','stop_id', 'stop_sequence', 'arrival_time','departure_time','point_distance', 'individual_time']])
processed_trip_df.to_csv('Dataset/stop_time3.txt', header=True, index=None, sep=',', mode='a') # type: ignore