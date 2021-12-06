import folium
import geopandas as gpd

# import base64  # import this if you want to embed image directly in map

def build_map(exif_df, img_dir, sample_rate=1):
    """
    Call this function to generate the UI (writes an .html map object).
    :param exif_df: In-memory dataframe that has the exif data and cow counts
    :param img_dir: Directory where ANNOTATED images are stored (probably s3)
    :param sample_rate: Preserves only every nth image. Used to ensure minimal overlap
    :return: writes map in .html
    """
    # convert the pandas dataframe into a geopandas dataframe
    gdf = gpd.GeoDataFrame(exif_df, crs="EPSG:4326", geometry=exif_df["bbox_poly_geom"])

    # TODO: Adjust the sampling rate so that we are only counting field of views that have little to no overlap
    filtered_gdf = gdf.iloc[::sample_rate, :]

    # TODO: Define map center and zoom
    map_center_coord = [39.36395608, -107.0395296]  # [lat, long]
    map = folium.Map(map_center_coord, zoom_start=18, tiles='cartodbpositron')

    # Add markers, cow counts, and image thumbnails for every image to the map.
    for c_lat, c_long, img_name, cow_count in zip(filtered_gdf["lat_dd"],
                                                  filtered_gdf["long_dd"],
                                                  filtered_gdf["filename"],
                                                  filtered_gdf["cow_count"]):
        # Display a link to the annotated image in the tooltip
        img_url = img_dir + img_name
        popup_url = "<a href=" + img_url + ">" + str(cow_count) + " cows detected</a>"

        # uncomment this instead if you want to embed images in the map file (makes file size very big)
        # encoded = base64.b64encode(open(img_dir + img_name, 'rb').read())
        # html = '<img src="data:image/png;base64,{}">'.format
        # iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=400, height=225)
        # popup = folium.Popup(iframe, max_width=400)

        folium.Marker(location=[c_lat, c_long], tooltip="Cow count (Yolov5):" + str(cow_count), popup=popup_url,
                      icon=folium.Icon(color='gray')).add_to(map)  # set popup=popup if you just want to embed thumbnail

    # Plot bounding box (i.e. field of view) polygons
    folium.GeoJson(filtered_gdf["geometry"]).add_to(map)

    # Writes out html map object into current working directory (can be the same s3 bucket!)
    map.save('/var/www/s3/livestalk_map_bytes.html')

    # Function can also return the map object directly, just uncomment below line
    # return map

