CREATE TABLE routes (
    route_id VARCHAR(255) PRIMARY KEY,
    agency_id VARCHAR(255),
    route_short_name VARCHAR(255),
    route_long_name TEXT,
    route_desc TEXT,
    route_type INTEGER,
    route_url TEXT,
    route_color VARCHAR(6),
    route_text_color VARCHAR(6),
    route_sort_order INTEGER,
    continuous_pickup INTEGER,
    continuous_drop_off INTEGER
);

CREATE USER gtadmin2 WITH PASSWORD 'gtfs####££££';
GRANT ALL PRIVILEGES ON DATABASE gtfs_del TO gtadmin2;