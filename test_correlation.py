from copernicus_service import search_sentinel1_images, parse_item_metadata
from correlation_service import calculate_time_window, filter_ais_in_bbox, correlate_sar_with_ais
from ais_service import get_access_token, fetch_live_positions

if __name__ == "__main__":
    # Target geographic area: Northern Norway / Troms coast
    # [min_lon, min_lat, max_lon, max_lat]
    bbox = [18.0, 69.0, 19.0, 70.0]

    print("Fetching satellite pass metadata from Copernicus (looking back 4 days)...")
    # Uses the updated dynamic search signature (days_back=4)
    results = search_sentinel1_images(bbox, days_back=4, collection_id="sentinel-1-grd")

    if results:
        latest_pass = results[0]
        metadata = parse_item_metadata(latest_pass)
        sat_time = metadata["datetime"]
        sat_bbox = metadata["bbox"]

        # Calculate temporal query window around satellite pass (+/- 15 mins)
        start_time, end_time = calculate_time_window(sat_time, margin_minutes=15)

        print("\n--- Correlation Setup ---")
        print(f"Satellite ID:       {metadata['id']}")
        print(f"Satellite Time:     {sat_time}")
        print(f"AIS Query Window:   {start_time.strftime('%H:%M:%S')} to {end_time.strftime('%H:%M:%S')} UTC")
        print(f"Footprint BBox:     {sat_bbox}")

        # Authenticate and fetch real AIS positions from BarentsWatch
        print("\nAuthenticating with BarentsWatch...")
        token = get_access_token()

        if token:
            print("Fetching live AIS positions...")
            raw_ais_data = fetch_live_positions(token)

            if raw_ais_data:
                records = raw_ais_data if isinstance(raw_ais_data, list) else raw_ais_data.get("features", [])
                matched_vessels = filter_ais_in_bbox(records, sat_bbox)
                print(f"Filtered {len(matched_vessels)} AIS vessels inside footprint.")

                # Simulated SAR radar detections from the Sentinel-1 image
                simulated_sar_detections = [
                    {"id": "SAR_TARGET_001", "lat": 69.7626, "lon": 16.6648},
                    {"id": "SAR_TARGET_002", "lat": 69.8500, "lon": 17.5000}
                ]

                print("\n--- Running Dark Ship Correlation Engine ---")
                correlation_results = correlate_sar_with_ais(simulated_sar_detections, matched_vessels, max_distance_km=1.5)

                print("\nVerified Vessels (Matched AIS + SAR):")
                for item in correlation_results["verified_vessels"]:
                    print(f"  [+] {item['name']} (MMSI: {item['mmsi']}) - Distance: {item['distance_km']} km")

                print("\nDARK SHIPS DETECTED (SAR Target with NO AIS):")
                for item in correlation_results["dark_ships"]:
                    print(f"  [!] ALERT: {item['sar_id']} at ({item['lat']}, {item['lon']}) - NO MATCHING AIS!")
        else:
            print("Failed to acquire BarentsWatch access token. Check your .env credentials.")
    else:
        print("No satellite passes found in the specified timeframe.")