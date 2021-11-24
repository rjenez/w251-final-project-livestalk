# %%

# Standard imports + exif tool parser
from os import listdir
import pandas as pd
import exiftool

# Field of view calculation dependencies
from math import degrees, radians, atan
from pyproj import Proj
from camera_calculator import CameraCalculator

# Imports for the UI
import folium
import geopandas as gpd
from shapely.geometry import Polygon
import base64


# pd.set_option('display.float_format', lambda x: '%.5f' % x) # suppress scientific notation to properly view utm

def unpack_bbox(bbox):
    """
    Takes in vector object from camera_calculator.py
    :param bbox:
    :return: Polygon object which is used to plot on folium map
    """
    x_list = []
    y_list = []
    for i, p in enumerate(bbox):
        x_list.append(p.x)
        y_list.append(p.y)
    # TODO: Ensure correct projection
    pp2 = Proj("+proj=utm +zone=10 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    long_list, lat_list = pp2(x_list, y_list, inverse=True)
    bbox_geom = Polygon(zip(long_list, lat_list))
    return bbox_geom


def build_map():
    """
    Reads all exif data from all images in a directory and returns a map with relevant features
    :return: .html file containing the final livestalk UI
    """
    # Set the directory where annotated images live
    # TODO: Adjust this for S3 and proper location

    image_dir = "test_images"
    dji_images = listdir(image_dir)
    dji_images = [image_dir + "/" + img for img in dji_images]  # read images from S3

    # Grab the metadata for all .JPGs in the directory
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(dji_images)

    exif_df = pd.DataFrame.from_dict(metadata)

    # keep only necessary fields for bbox calculation
    exif_df = exif_df[["File:FileName", "MakerNotes:CameraPitch", "MakerNotes:CameraYaw", "MakerNotes:CameraRoll",
                       "EXIF:GPSAltitude", "EXIF:GPSLatitude", "EXIF:GPSLongitude"]]

    # TODO: MAKE SURE THE SIGNS ON LAT LONG ARE CORRECT
    exif_df["EXIF:GPSLongitude"] = -1 * exif_df["EXIF:GPSLongitude"]

    # Lat Long conversion from decimal degrees to UTM
    # TODO: First, set the UTM zone object
    pp = Proj("+proj=utm +zone=10 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Convert the centroid lat, long to UTM
    c_x_utm, c_y_utm = pp(exif_df["EXIF:GPSLongitude"].values, exif_df["EXIF:GPSLatitude"].values)
    exif_df["centroid_x_utm"] = c_x_utm
    exif_df["centroid_y_utm"] = c_y_utm - 10000000  # TODO: Figure out why northing gives incorrect value (+10,000,000)

    # DJ Mavic Mini and DJ Mavic Pro sensor specs. These are all fixed values
    img_width_max_px = 4000
    img_height_max_px = 3000
    img_width_cropped = 4000
    img_height_cropped = 2250
    sensor_width_mm = 6.3  # not contained in exif
    sensor_height_mm = 4.7  # not contained in exif
    focal_length = 4.49

    # We need to calculate the horizontal and vertical field of view from the cropped or effective sensor size
    # see: https://mavicpilots.com/threads/mavic-mini-focal-length-versus-field-of-view.85622/
    cropped_sensor_width = img_width_cropped / (img_width_max_px / sensor_width_mm)
    cropped_sensor_height = img_height_cropped / (img_height_max_px / sensor_height_mm)
    fov_h = degrees(atan(cropped_sensor_width / (2 * focal_length))) * 2
    fov_v = degrees(atan(cropped_sensor_height / (2 * focal_length))) * 2

    exif_df["fov_h"] = fov_h
    exif_df["fov_v"] = fov_v

    # Calculate the field of view using the getBoundingPolygon method in camera_calculator.py
    c = CameraCalculator()

    exif_df["bbox_vec"] = exif_df.apply(lambda row: c.getBoundingPolygon(
        radians(row["fov_h"]),
        radians(row["fov_v"]),
        row["EXIF:GPSAltitude"],
        radians(row["MakerNotes:CameraYaw"]),
        radians(row["MakerNotes:CameraRoll"]),
        radians(row["MakerNotes:CameraPitch"]),
        row["centroid_x_utm"],
        row["centroid_y_utm"]
    ), axis=1)

    # Convert the resultant field of view vector into a valid geometry format for geopandas
    exif_df["bbox_poly_geom"] = exif_df.apply(lambda row: unpack_bbox(row["bbox_vec"]), axis=1)
    gdf = gpd.GeoDataFrame(exif_df, crs="EPSG:4326", geometry=exif_df["bbox_poly_geom"])

    # TODO: Adjust the sampling rate so that we are only counting field of views that have little to no overlap
    sampling_rate = 1  # fps
    filtered_gdf = gdf.iloc[::sampling_rate, :]

    # TODO: Define map center and zoom
    centroid_coord = [37.36204, -122.07071]
    m = folium.Map(centroid_coord, zoom_start=18, tiles='cartodbpositron')

    # Original dataframe is now filtered for the proper sampling frequency
    folium.GeoJson(filtered_gdf["geometry"]).add_to(m)
    folium.LatLngPopup().add_to(m)

    # TODO: Add thumbnails
    # Ensure image is base-64 encoded (This might be an optional step)
    encoded = base64.b64encode(open('test_images/DJI_0244.JPG', 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=4000, height=2250)
    popup = folium.Popup(iframe, max_width=400)

    # This adds a clickable icon
    folium.Marker(location=[37.36204, -122.07071], tooltip=html, popup=popup,
                  icon=folium.Icon(color='gray')).add_to(m)

    # Saving map in current working directory
    m.save('livestalk_map.html')


if __name__ == "__main__":
    build_map()
