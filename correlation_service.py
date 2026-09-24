import math
from datetime import timedelta

def calculate_time_window(satellite_datetime, margin_minutes=15):
    """
    Calculates a temporal query window centered around a satellite pass timestamp.

    Args:
        satellite_datetime (datetime.datetime): Exact UTC timestamp of the satellite pass.
        margin_minutes (int, optional): Time buffer in minutes before/after the pass. Defaults to 15.

    Returns:
        tuple: (start_time, end_time) as timezone-aware datetime objects.
    """
    start_time = satellite_datetime - timedelta(minutes=margin_minutes)
    end_time = satellite_datetime + timedelta(minutes=margin_minutes)
    return start_time, end_time


def filter_ais_in_bbox(ais_records, bbox):
    """
    Filters raw AIS vessel records to keep only those falling within a geographic bounding box.
    Handles multiple standard formats: flat dictionaries, nested structures, and GeoJSON Features.

    Args:
        ais_records (list or dict): Raw vessel data retrieved from BarentsWatch API.
        bbox (list of float): Bounding box [min_lon, min_lat, max_lon, max_lat].

    Returns:
        list: Filtered AIS vessel records located inside the specified footprint.
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    filtered_records = []

    # Unwrap if payload is formatted as a GeoJSON FeatureCollection dictionary
    if isinstance(ais_records, dict) and "features" in ais_records:
        ais_records = ais_records["features"]

    if not isinstance(ais_records, list):
        return filtered_records

    for record in ais_records:
        lat, lon = None, None

        # Extract coordinates across varying API response schemas
        if "latitude" in record and "longitude" in record:
            lat = record.get("latitude")
            lon = record.get("longitude")
        elif "lat" in record and "lon" in record:
            lat = record.get("lat")
            lon = record.get("lon")
        elif "geometry" in record and "coordinates" in record["geometry"]:
            coords = record["geometry"]["coordinates"]
            if len(coords) >= 2:
                lon, lat = coords[0], coords[1]

        # Spatial bounding box boundary check
        if lat is not None and lon is not None:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                filtered_records.append(record)

    return filtered_records


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two geographic points on Earth 
    using the Haversine formula.

    Args:
        lat1 (float): Latitude of point 1 in decimal degrees.
        lon1 (float): Longitude of point 1 in decimal degrees.
        lat2 (float): Latitude of point 2 in decimal degrees.
        lon2 (float): Longitude of point 2 in decimal degrees.

    Returns:
        float: Distance between the two coordinates in kilometers.
    """
    EARTH_RADIUS_KM = 6371.0

    # Convert degrees to radians
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    # Trigonometric Haversine calculation
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return EARTH_RADIUS_KM * c


def correlate_sar_with_ais(sar_detections, ais_vessels, max_distance_km=1.5):
    """
    Correlates radar targets extracted from SAR satellite imagery against active AIS vessel tracks.
    Identifies verified vessels (matching AIS broadcast) and flags potential 'Dark Ships'.

    Args:
        sar_detections (list of dict): Radar targets [{'id': 'SAR_001', 'lat': 69.5, 'lon': 18.5}, ...]
        ais_vessels (list of dict): AIS vessel records inside the satellite footprint.
        max_distance_km (float, optional): Maximum matching distance threshold. Defaults to 1.5 km.

    Returns:
        dict: Contains 'verified_vessels' (matched) and 'dark_ships' (unmatched radar targets).
    """
    verified_vessels = []
    dark_ships = []

    for sar in sar_detections:
        sar_lat = sar["lat"]
        sar_lon = sar["lon"]
        closest_ais = None
        min_dist = float("inf")

        # Find the nearest AIS vessel to the current radar target
        for vessel in ais_vessels:
            props = vessel.get("properties", vessel) if isinstance(vessel, dict) else {}
            vessel_lat = props.get("latitude", props.get("lat"))
            vessel_lon = props.get("longitude", props.get("lon"))

            if vessel_lat is not None and vessel_lon is not None:
                dist = haversine_distance_km(sar_lat, sar_lon, vessel_lat, vessel_lon)
                if dist < min_dist:
                    min_dist = dist
                    closest_ais = vessel

        # If closest AIS vessel is within distance threshold, classify as Verified
        if closest_ais and min_dist <= max_distance_km:
            props = closest_ais.get("properties", closest_ais) if isinstance(closest_ais, dict) else {}
            verified_vessels.append({
                "sar_id": sar["id"],
                "mmsi": props.get("mmsi", props.get("mmsiNumber")),
                "name": props.get("name", props.get("vesselName")),
                "distance_km": round(min_dist, 3)
            })
        else:
            # No AIS broadcast nearby -> Flag as Dark Ship Anomaly
            dark_ships.append({
                "sar_id": sar["id"],
                "lat": sar_lat,
                "lon": sar_lon,
                "anomaly": "DARK_SHIP"
            })

    return {
        "verified_vessels": verified_vessels,
        "dark_ships": dark_ships
    }