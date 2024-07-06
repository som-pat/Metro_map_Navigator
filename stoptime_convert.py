import pandas as pd
time = pd.read_csv('Dataset/stop_times.txt')

def normalize_time(time_str):
    
    h, m, s = map(int, time_str.split(':'))
    # Normalize hours if they are 24 or more
    if h >= 24:
        h = h % 24
    # Return the normalized time string
        
    return f"{h:02}:{m:02}:{s:02}"


time['arrival_time'] = time['arrival_time'].apply(normalize_time)
time['departure_time'] = time['departure_time'].apply(normalize_time)


time.to_csv('Dataset/stop_time2.txt', header=True, index=None, sep=',', mode='a') # type: ignore