# gtfs_webapp

#### This project is a web application that displays metro routes and stops for a city using FastAPI, Docker, and PostgreSQL. Users can input start and end points to find the shortest route, and the map dynamically updates to show the route and stops.

## Features

- Display metro stops on a map.
- Find and display the shortest route between two points.
- Highlight start and end points on the map.
- Use Docker for containerization and PostgreSQL as the database.

Project Structure
``` bash
project_root/
│
├── Dataset/
│   ├── agency.txt
│   ├── calendar.txt
│   ├── routes4.txt
│   ├── shapes.txt
│   ├── stop_time2.txt
│   ├── stops.txt
│   └── trips.txt
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── Extract_load.py
└── transit.py
```

##Technologies Used:

-Frontend: Leaflet.js, HTML, CSS, JavaScript
-Backend: FastAPI, Python
-Database: PostgreSQL
-Containerization: Docker, Docker Compose
