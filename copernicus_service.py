from datetime import datetime, timedelta, timezone
from pystac_client import Client

# Copernicus Data Space Ecosystem STAC API Endpoint
STAC_URL = "https://catalogue.dataspace.copernicus.eu/stac"

def search_sentinel1_images(bbox, days_back=3, collection_id="sentinel-1-grd"):
    """
    Searches Copernicus STAC API for Sentinel-1 Synthetic Aperture Radar (SAR) 
    ground range detected (GRD) satellite passes over a given bounding box.

    Args:
        bbox (list of float): Bounding box [min_lon, min_lat, max_lon, max_lat].
        days_back (int, optional): Lookback window in days from current UTC time. Defaults to 3.
        collection_id (str, optional): Target STAC collection name. Defaults to "sentinel-1-grd".

    Returns:
        list of pystac.Item: List of matching satellite pass items ordered by recency.
    """
    # Calculate dynamic temporal query window based on current UTC time
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_back)

    # Format timestamps according to ISO-8601 standard required by STAC
    datetime_str = f"{start_date.strftime('%Y-%m-%d')}T00:00:00Z/{end_date.strftime('%Y-%m-%d')}T23:59:59Z"

    # Open STAC catalog connection
    catalog = Client.open(STAC_URL)
    
    # Execute spatio-temporal search query
    search = catalog.search(
        collections=[collection_id],
        bbox=bbox,
        datetime=datetime_str
    )
    
    return list(search.items())


def parse_item_metadata(item):
    """
    Extracts essential operational metadata and visual asset URLs from a STAC Item.

    Args:
        item (pystac.Item): A STAC Item object returned by the Copernicus search.

    Returns:
        dict: Parsed metadata including satellite ID, capture timestamp, bbox, and thumbnail URL.
    """
    assets = item.assets
    
    # Retrieve thumbnail image URL if present in asset catalogue
    preview_url = assets["thumbnail"].href if "thumbnail" in assets else None

    return {
        "id": item.id,
        "datetime": item.datetime,
        "bbox": item.bbox,
        "geometry": item.geometry,
        "preview_url": preview_url,
        "assets_count": len(assets)
    }