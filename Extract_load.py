# Create dummy Database and  grant it a user 

# -- To create dedicated admin and pw for the db 
# CREATE USER transitadmin WITH PASSWORD 'gtfsuser0000';
# GRANT ALL PRIVILEGES ON DATABASE gtfs_del TO transitadmin;


# Library
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os
# Route.txt Conversion
routes = pd.read_csv('Dataset/routes.txt')
def seperator(route_long_name):
    parts = route_long_name.split('_')
    if 'RAPID' in parts:
        parts[0] ='PURPLE'
    if 'ORANGE/AIRPORT' in parts:
        parts[0] ='ORANGE'
    if 'GRAY' in parts:
        parts[0] ='#0C0C0C'
    if 'YELLOW' in parts:
        parts[0] = '#750E21'
    if 'MAGENTA' in parts:
        parts[0] = '#720455'

    color = parts[0] if len(parts)>1 else None
    if 'to' in parts[-1]:
        rt = parts[-1].split(' to ')
        start_point = rt[0]
        end_point = rt[1]
    else:
        start_point=end_point=None
    
    return pd.Series([color,start_point,end_point])

routes[['route_color','start_point','end_point']] = routes['route_long_name'].apply(seperator)
routes = routes.sort_values(by=['route_color'])
# empty the text file if previously used to prevent duplication
routes.to_csv('Dataset/routes4.txt', header=True, index=None, sep=',', mode='a') # type: ignore

# Stop_times.txt conversion
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

# empty the text file if previously used to prevent duplication
time.to_csv('Dataset/stop_time2.txt', header=True, index=None, sep=',', mode='a') # type: ignore
 




# Define the database connection parameters,change
# db_params = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'database': os.getenv('DB_NAME', 'gtfs_del'),
#     'user': os.getenv('DB_USER', 'transitadmin'),
#     'password': os.getenv('DB_PASS', 'gtfsuser0000')
# }

db_params = {
    'host': "localhost",
    'database':"gtfs_del",
    'user': "transitadmin",
    'password': 'gtfsuser0000'
}

# Create a connection to the PostgreSQL server
conn = psycopg2.connect(
    host=db_params['host'],
    database=db_params['database'],
    user=db_params['user'],
    password=db_params['password']
)
# Create a cursor object
cur = conn.cursor()

# Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
conn.set_session(autocommit=True)

# Commit the changes and close the connection to the default database
conn.commit()
cur.close()
conn.close()



# db_params['database'] = 'gtfs_del'
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

# Define the file paths for your txt files

csv_files = {
    'agency':'Dataset/agency.txt',
    'calendar':'Dataset/calendar.txt',
    'route': 'Dataset/routes4.txt',
    'shape': 'Dataset/shapes.txt',
    'stop_times':'Dataset/stop_time2.txt',
    'stops': 'Dataset/stops.txt',
    'trips': 'Dataset/trips.txt'
}



# Loop through the CSV files and import them into PostgreSQL
for table_name, file_path in csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data from {file_path} has been uploaded to the {table_name} table.")