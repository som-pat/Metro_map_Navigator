-- To create dedicated admin and pw for the db 
CREATE USER transitadmin WITH PASSWORD 'gtfsuser0000';
GRANT ALL PRIVILEGES ON DATABASE gtfs_del TO transitadmin;