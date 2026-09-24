from copernicus_service import search_sentinel1_images, parse_item_metadata

if __name__ == "__main__":
    # Bounding box: Northern Norway / Troms coast
    bbox = [18.0, 69.0, 19.0, 70.0]
    start_date = "2026-09-20"
    end_date = "2026-09-24"

    print("Searching for Sentinel-1 GRD satellite passes...")
    results = search_sentinel1_images(bbox, start_date, end_date, collection_id="sentinel-1-grd")
    
    print(f"\nFound {len(results)} satellite passes!")
    
    if results:
        latest_pass = results[0]
        metadata = parse_item_metadata(latest_pass)
        
        print("\n--- Parsed Metadata for Latest Pass ---")
        print(f"ID:           {metadata['id']}")
        print(f"Timestamp:    {metadata['datetime']}")
        print(f"Bounding Box: {metadata['bbox']}")
        print(f"Preview URL:  {metadata['preview_url']}")
        print(f"Total Assets: {metadata['assets_count']}")