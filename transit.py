# uvicorn transit:app --reload
from fastapi import FastAPI, status, Request, Form
from typing import List
import uvicorn
import psycopg2
import heapq
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
import os

DATABASE_URL = "postgresql://transitadmin:gtfsuser0000@localhost/gtfs_del"
templates = Jinja2Templates(directory="templates")
app = FastAPI()
# DATABASE_URL = os.getenv('DATABASE_URL')


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

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

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
        print(route_id)
        shape_id = route_shape_map[route_id]

        if shape_id in shapes:
            route_cor.append({
                'route_id':route_id,
                'color':route[1],
                'points':shapes[shape_id]
            })

    return templates.TemplateResponse("map.html", {
        "request": request, 
        "stops": stops, 
        "routes":route_cor,
        'short_path' :[]})





def construct_graph():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch stops data
    cur.execute("SELECT stop_id FROM stops")
    stops = cur.fetchall()
    
    # Fetch stop_times and trips data to construct the graph
    cur.execute("""
        SELECT st1.stop_id, st2.stop_id, st1.shape_dist_traveled, t.route_id 
        FROM stop_times st1
        JOIN stop_times st2 ON st1.trip_id = st2.trip_id AND st1.stop_sequence + 1 = st2.stop_sequence
        JOIN trips t ON st1.trip_id = t.trip_id
    """)
    stop_connections = cur.fetchall()
    # print(stop_connections)
    cur.close()
    conn.close()
    
    graph = {stop[0]: [] for stop in stops}
    
    for connection in stop_connections:        
        graph[connection[0]].append((connection[1], connection[2]))
        graph[connection[1]].append((connection[0], connection[2]))  # Assuming undirected graph    
    

    return graph




def ShortestPath(graph, start, end):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
                
    path, current_node = [], end
    while previous_nodes[current_node] is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    if path:
        path.append(start)
    
    return path[::-1]


@app.post('/searchRoute',response_class=JSONResponse)
async def searchRoute(request: Request, start_point: str = Form(...), end_point: str = Form(...)):
 
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT stop_id FROM stops WHERE stop_name = %s", (start_point,))
    start = cur.fetchone()[0] # type: ignore 
    cur.execute("SELECT stop_id FROM stops WHERE stop_name = %s", (end_point,))
    end = cur.fetchone()[0] # type: ignore 
    cur.close()
    conn.close()
    
    graph = construct_graph()
    shortest_path= ShortestPath(graph, start, end)

    path_coords = []
    route_name = []
    conn = get_db_connection()
    stopcur = conn.cursor()
    for stop_id in shortest_path:
        stopcur.execute("SELECT stop_lat, stop_lon, stop_name FROM stops WHERE stop_id = %s", (stop_id,))
        stop = stopcur.fetchone()
        path_coords.append([stop[0], stop[1]]) # type: ignore
        route_name.append(stop[2]) # type: ignore
    stopcur.close()
    conn.close()
    # print(path_coords)
    return JSONResponse(content={"path": path_coords,"routeName":route_name})      






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
