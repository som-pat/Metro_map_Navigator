from pydantic import BaseModel
from typing import Optional

class Route(BaseModel):
    route_id: int
    route_short_name: Optional[str] = None
    route_long_name: Optional[str] = None
    route_type: Optional[int] = None

class Stops(BaseModel):
    stop_id :int
    stop_name: Optional[str] = None
    stop_lat: float
    stop_lon: float

class Trips(BaseModel):
    route_id:int
    service_id: str
    trip_id:int
    shape_id:str
    wheelchair_accessible:Optional[int] = None
    bikes_allowed:Optional[int] = None


class Shapes(BaseModel):
    shape_id :str
    shape_pt_lat:float
    shape_pt_lon:float
    shape_pt_sequence:int
    shape_dist_traveled:Optional[float] = None

class Stop_times(BaseModel):
    trip_id:int
    arrival_time: str
    departure_time:str
    stop_id:int
    stop_sequence: int
    pickup_type: Optional[int]=None
    drop_off_type: Optional[int]=None
    shape_dist_traveled:float
    timepoint:int

    