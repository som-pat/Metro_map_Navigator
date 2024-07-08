# import csv
# import psycopg2

# def load_data(filepath):
#     conn = psycopg2.connect(
#         dbname="gtfs_del",
#         user="gtadmin2",
#         password='',
#         host="localhost"
#     )
#     cur = conn.cursor()
#     with open(filepath, 'r', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         next(reader)  # Skip the header row
#         for row in reader:
            
#             cur.execute(
#                 """
#                 INSERT INTO routes (route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color, route_sort_order, continuous_pickup, continuous_drop_off)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (route_id) DO NOTHING;
#                 """,
#                 row
#             )
#     conn.commit()
#     cur.close()
#     conn.close()

# load_data('')


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


@app.post('/search_route', response_class=HTMLResponse)
async def search_route(request: Request):
    form = await request.form()
    start_point = form.get("start_point")
    end_point = form.get("end_point")
    

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT stop_id FROM stops WHERE stop_name = %s", (start_point,))
    start = cur.fetchone()[0] # type: ignore 
    cur.execute("SELECT stop_id FROM stops WHERE stop_name = %s", (end_point,))
    end = cur.fetchone()[0] # type: ignore 
    cur.close()
    conn.close()
    
    graph = construct_graph()
    shortest_path = dijkstra(graph, start, end)
    
    conn = get_db_connection()
    stopcur = conn.cursor()
    stopcur.execute("SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops")
    stops = stopcur.fetchall()
    stopcur.close()
    conn.close()
    
    
    return templates.TemplateResponse("map.html", {
        "request": request,
        "stops": stops,
        'routes':[],  
        "short_path": shortest_path, 
    })



def construct_graph_with_time():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch stops data
    cur.execute("SELECT stop_id FROM stops")
    stops = cur.fetchall()
    
    # Fetch stop_times and trips data to construct the graph
    cur.execute("""
        SELECT st1.stop_id, st2.stop_id,st2.arrival_time::time as t1, st1.departure_time::time as t2, st1.shape_dist_traveled, 
	t.route_id,EXTRACT(EPOCH FROM (st2.arrival_time::time - st1.departure_time::time)) as travel_time
        FROM stop_times st1
        JOIN stop_times st2 
            ON st1.trip_id = st2.trip_id 
            AND st1.stop_sequence + 1 = st2.stop_sequence
		JOIN trips t ON st1.trip_id = t.trip_id
Order by st1.stop_id, st2.stop_id;
    """)
    stop_connections = cur.fetchall()
    cur.close()
    conn.close()
    # print(stop_connections)
    graph = {stop[0]: [] for stop in stops}
    
    for connection in stop_connections:
        if connection[2] is not None:
            time = float(connection[2]) 
            graph[connection[0]].append((connection[1], time))
            # graph[connection[1]].append((connection[0], time))

    return graph



def dijkstra_with_td(graph, start, end):
    queue = [(0,0, start)]
    distance = {node: float('inf') for node in graph}
    time = {node: float('inf') for node in graph}
    distance[start] = 0
    time[start] = 0
    previous_nodes = {node: None for node in graph}
    i=0
    while queue:
        current_distance, current_time, current_node = heapq.heappop(queue)
        if current_node == end:
            break

        if (current_distance > distance[current_node]) and (current_time > time[current_node]):
            continue
        
        for neighbor, wt_distance, wt_time in graph[current_node]:
            # Combine distance and time with given weights
            print(neighbor)
            total_distance = current_distance+ wt_distance
            total_time = current_time + wt_time
            
            
            print(total_distance)
            print(total_time)

            if total_distance < distance[neighbor] or total_time<time[neighbor] :
                distance[neighbor] = total_distance
                time[neighbor] = total_time
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (total_distance, total_time, neighbor))

    path, current_node = [], end
    while previous_nodes[current_node] is not None:
        path.append(current_node)   
        current_node = previous_nodes[current_node]
    if path:
        path.append(start)
    return path[::-1]

def dijkstraextra(graph, start, end):
    queue = [(0, 0, start)]  # ( total_time, total_distance,node)
    distances = {node: float('infinity') for node in graph}
    times = {node: float('infinity') for node in graph}
    distances[start] = 0
    times[start] = 0
    previous_nodes = {node: None for node in graph}
    
    while queue:
        current_time, current_distance,current_node = heapq.heappop(queue)
        
        if current_node == end:
            break
        
        if  current_time > times[current_node]:
            continue
        
        for neighbor, distance, travel_time in graph[current_node]:
            print(neighbor)
            total_distance = current_distance + distance
            total_time = current_time + travel_time
            
            if total_time < times[neighbor] or (total_time == times[neighbor] and total_distance < distances[neighbor]):
                distances[neighbor] = total_distance
                times[neighbor] = total_time
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (total_time, total_distance, neighbor))
                
    path, current_node = [], end
    while previous_nodes[current_node] is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    if path:
        path.append(start)
    return path[::-1]

# Example usage:
# graph = construct_graph_with_time()
# path = dijkstra(graph, 'start_node', 'end_node', distance_weight=0.6, time_weight=0.4)    


# print(dijkstraextra(construct_graph_with_time(), 12, 202))

def dijkstra_with_time(graph, start, end):
    queue = [(0, start)]  # (travel_time, stop_id)
    travel_times = {node: float('inf') for node in graph}
    travel_times[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        current_travel_time, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, travel_time in graph[current_node]:
            new_travel_time = current_travel_time + travel_time
            print(neighbor,new_travel_time)
            if new_travel_time < travel_times[neighbor]:
                travel_times[neighbor] = new_travel_time
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (new_travel_time, neighbor))
    
    path, current_node = [], end
    while previous_nodes[current_node] is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    if path:
        path.append(start)
    return path[::-1], travel_times[end]
