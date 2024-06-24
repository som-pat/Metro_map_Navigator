# Library
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text

# Define the database connection parameters,change
db_params = {
    'host': "localhost",
    'database':"gtfs_del",
    'user': "gtadmin2",
    'password': 'gtfs####££££'
}
# gtfs####££££
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
    'route': 'Dataset/routes.txt',
    'shape': 'Dataset/shapes.txt',
    'stop_times':'Dataset/stop_times.txt',
    'stops': 'Dataset/stops.txt',
    'trips': 'Dataset/trips.txt'
}

# Load and display the contents of each CSV file to check
for table_name, file_path in csv_files.items():
    df = pd.read_csv(file_path)

# Loop through the CSV files and import them into PostgreSQL
for table_name, file_path in csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)