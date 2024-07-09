# Metro_map_Navigator

#### This project is a web application that displays metro routes and stops for a city using FastAPI, Docker, and PostgreSQL. Users can input start and end points to find the shortest route, and the map dynamically updates to show the route and stops.

## Features

- Display metro stops on a map.
- Zoom up and down restricted to a certain level.
- Find and display the shortest route between two points based on distance and time.
- Red point indicates Start-Point and Green point indicates End-Point
- Highlight start and end points on the map.
- Use Docker for containerization and PostgreSQL as the database.

- Full Map of the Metro Line
![Map_metro](https://github.com/som-pat/Metro_map_Navigator/assets/53874321/708147fd-0f24-4031-a62c-2a45b709341c)

- Detailed Route map, input and summary shown only at a certain zoom level
![detailed_map](https://github.com/som-pat/Metro_map_Navigator/assets/53874321/435a6840-7cae-4c98-b5f2-5c9ee8ef22c4)

- Displaying the Shortest path between selected start and end point
![Route display](https://github.com/som-pat/Metro_map_Navigator/assets/53874321/1ced9a9e-e0e1-4b2d-a55a-24de8c665098)


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
|
├──Static/
|  ├──styles.css
|
├──Templates/
|  ├──map.html
|
|  
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── Extract_load.py
└── transit.py
```

## Technologies Used:

- Frontend: Leaflet.js, HTML, CSS, JavaScript
- Backend: FastAPI, Python
- Database: PostgreSQL
- Containerization: Docker, Docker Compose

