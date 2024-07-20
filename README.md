# Metro_map_Navigator

#### This project is a web application that displays metro routes and stops for a city using FastAPI, Leaflet.js and PostgreSQL. Users can input start and end points to find the shortest route, and the map dynamically updates to show the route and stops.

## Features

- Display metro stops on a map.
- Zoom up and down restricted to a certain level.
- Find and display the shortest route between two points based on distance and time.
- Redpoint indicates Start-Point and Green point indicates End-Point
- Highlight start and end points on the map.
- Use Docker for containerization and PostgreSQL as the database.
  

- Full Map of the Metro Line
![Map_metro](https://github.com/som-pat/Metro_map_Navigator/assets/53874321/708147fd-0f24-4031-a62c-2a45b709341c)

- Detailed Route map, input and summary shown only at a certain zoom level
![detailed_map](https://github.com/som-pat/Metro_map_Navigator/assets/53874321/435a6840-7cae-4c98-b5f2-5c9ee8ef22c4)

- Displaying the Shortest path between selected [red] start and [green]end point
![updated route display](https://github.com/user-attachments/assets/d28bc92b-bbbc-44c6-8b73-1a39afd93f3d)



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
├──Static/
│  ├──styles.css
│
├──Templates/
│  ├──map.html
│
│  
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

#### This project follows the guidelines from the General Transit Feed Specification (GTFS) for its working and the data used is static, hence accuracy is not guaranteed
##### GTFS link 
- [https://gtfs.org/]
- [https://developers.google.com/transit/gtfs]
##### Static GTFS dataset
- [https://otd.delhi.gov.in/data/staticDMRC/]
        
##### Delhi Metro route
- [https://delhimetrorail.info/Images/delhimetro-map_eng.jpg] 