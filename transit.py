# uvicorn transit:app --reload
from fastapi import FastAPI, status, Request
from typing import List
import uvicorn
import psycopg2
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


DATABASE_URL = "postgresql://gtadmin2:gtfsgudu1212@localhost/gtfs_del"
templates = Jinja2Templates(directory="templates")
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn



@app.get('/status')
async def check_status():
    return 'Hello World'

@app.get('/routes', response_model=List[Route], status_code=status.HTTP_200_OK)
async def get_routes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT route_id,route_short_name,route_long_name,route_type,route_color,start_point,end_point FROM route ORDER BY route_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Route(
                route_id=row[0],
                route_short_name=row[1],
                route_long_name=row[2],
                route_type=row[3],
                route_color=row[4],
                start_point=row[5],
                end_point=row[6],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes  # Ensure the list is returned

@app.get('/stops', response_model=List[Stops], status_code=status.HTTP_200_OK)
async def get_stops():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops ORDER BY stop_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Stops(
                stop_id=row[0],
                stop_name=row[1],
                stop_lat=row[2],
                stop_lon=row[3],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes 


@app.get('/trips', response_model=List[Trips], status_code=status.HTTP_200_OK)
async def get_trips():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT route_id, service_id, trip_id, shape_id, wheelchair_accessible, bikes_allowed FROM trips ORDER BY route_id,trip_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Trips(
                route_id =row[0],
                service_id = row[1],
                trip_id = row[2],
                shape_id =row[3],
                wheelchair_accessible = row[4],
                bikes_allowed = row[5],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes 


@app.get('/trip_shape', response_model=List[Shapes], status_code=status.HTTP_200_OK)
async def get_trip_shape():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled FROM shape")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Shapes(
                shape_id = row[0],
                shape_pt_lat = row[1],
                shape_pt_lon = row[2],
                shape_pt_sequence = row[3],
                shape_dist_traveled = row[4],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes

@app.get('/Stop_times', response_model=List[Stop_times], status_code=status.HTTP_200_OK)
async def get_stop_times():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled,timepoint FROM stop_times ORDER BY trip_id,stop_id")
    rows = cur.fetchall()
    
    formatted_routes = []

    for row in rows:
        formatted_routes.append(
            Stop_times(
                trip_id = row[0],
                arrival_time = row[1],
                departure_time = row[2],
                stop_id =row[3],
                stop_sequence=row[4],
                pickup_type=row[5],
                drop_off_type=row[6],
                shape_dist_traveled=row[7],
                timepoint=row[8],
            )
        )

    cur.close()
    conn.close()

    return formatted_routes

@app.get('/', response_class=HTMLResponse)
async def get_map_stops(request: Request):
    conn = get_db_connection()
    stopcur = conn.cursor()
    routecur = conn.cursor()
    shapecur = conn.cursor()
    tripcur  = conn.cursor()

    # Fetch the stop data
    stopcur.execute("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops")
    stops = stopcur.fetchall()

    # Fetch the route data 
    routecur.execute("SELECT route_id,route_color FROM route Order By route_id")
    routes = routecur.fetchall()

    #Fetch the shape data
    shapecur.execute("SELECT shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence FROM shape ORDER BY shape_id, shape_pt_sequence")
    shape_points = shapecur.fetchall()

    # fetch the trip data
    tripcur.execute("Select route_id, shape_id FROM trips")
    trips = tripcur.fetchall()
    
    tripcur.close()
    shapecur.close()
    routecur.close()
    stopcur.close()
    conn.close()
    
    # Attach route's start & endpoint with coordinates
    # stop_coords = {stop[1]: (stop[2], stop[3]) for stop in stops}

    shapes = {}
    for point in shape_points:
        shape_id = point[0]
        if shape_id not in shapes:
            shapes[shape_id] = []
        shapes[shape_id].append([point[1], point[2]])
    

        # Map route_id to shape_id
    route_shape_map = {}
    for trip in trips:
        route_id = trip[0]
        shape_id = trip[1]
        if route_id not in route_shape_map:
            route_shape_map[route_id] = shape_id
    
    
    
    route_cor = []
    for route in routes:
        route_id = route[0]
        shape_id = route_shape_map[route_id]

        if shape_id in shapes:
            route_cor.append({
                'route_id':route_id,
                'color':route[1],
                'points':shapes[shape_id]
            })

    return templates.TemplateResponse("map.html", {"request": request, "stops": stops, 
                                                   "routes":route_cor,"shapes":shapes})






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
