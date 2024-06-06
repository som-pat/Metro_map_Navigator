import csv
import psycopg2

def load_data(filepath):
    conn = psycopg2.connect(
        dbname="gtfs_del",
        user="gtadmin2",
        password='gtfs####££££',
        host="localhost"
    )
    cur = conn.cursor()
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            
            cur.execute(
                """
                INSERT INTO routes (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color, route_sort_order, continuous_pickup, continuous_drop_off)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (route_id) DO NOTHING;
                """,
                row
            )
    conn.commit()
    cur.close()
    conn.close()

load_data('C:/Users/patra/Documents/gtfs_project_new/Dataset/routes.txt')

