# Exif extraction dependencies
import pandas as pd
from exif import Image

# Georeferencing dependencies
from math import degrees, radians, atan
from pyproj import Proj
from camera_calculator import CameraCalculator
from shapely.geometry import Polygon


def unpack_bbox(bbox):
    """
    Takes in vector object from camera_calculator.py
    :param bbox: vector object returned from camera_calulator.py methods
    :return: Polygon object which is used to plot on folium map
    """
    x_list = []
    y_list = []
    for i, p in enumerate(bbox):
        x_list.append(p.x)
        y_list.append(p.y)
    # Ensure this matches the projection in get_exif()
    pp2 = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    long_list, lat_list = pp2(x_list, y_list, inverse=True)
    bbox_geom = Polygon(zip(long_list, lat_list))
    return bbox_geom


def gps_dms_to_dd(image):
    """
    Quick and dirty function to convert exif lat long in dms to dd
    :param image: the image stored as bytes
    :return: (lat, long) tuple
    """
    long_degrees = image.get("gps_longitude")[0]
    long_minutes = image.get("gps_longitude")[1]
    long_seconds = image.get("gps_longitude")[2]
    long_dd = long_degrees + long_minutes / 60 + long_seconds / 3600

    lat_degrees = image.get("gps_latitude")[0]
    lat_minutes = image.get("gps_latitude")[1]
    lat_seconds = image.get("gps_latitude")[2]
    lat_dd = lat_degrees + lat_minutes / 60 + lat_seconds / 3600
    return lat_dd, -long_dd


def get_exif(image_bytes):
    """
    :param image_bytes: image variable stored as bytes
    :return: Single-row dataframe that can be appended to a blank global dataframe used to populate html map
    """
    # Convert bytes to image object using exif module
    image = Image(image_bytes)

    # Blank dataframe for storing exif and geo data
    exif_df = pd.DataFrame()

    exif_df["filename"] = [image.get("image_description")[14:]]  # just pull out "DJI_XXXX.JPG"
    exif_df["lat_dd"] = gps_dms_to_dd(image)[0]
    exif_df["long_dd"] = gps_dms_to_dd(image)[1]

    # All other variables are hardcoded for now since we can't read them from the in-memory exif
    exif_df["pitch"] = -90
    exif_df["yaw"] = 0
    exif_df["roll"] = 0
    exif_df["relative_altitude"] = 45.7

    # Lat Long conversion from decimal degrees to UTM
    # UTM zone is set for Basalt, CO (demo flyby location)
    # Use http://rcn.montana.edu/Resources/Converter.aspx to check the right zone
    pp = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Convert the centroid long, lat to UTM
    c_x_utm, c_y_utm = pp(exif_df["long_dd"].values, exif_df["lat_dd"].values)
    exif_df["centroid_x_utm"] = c_x_utm
    exif_df["centroid_y_utm"] = c_y_utm

    # DJ Mavic Mini and DJ Mavic Pro sensor specs. These are all fixed values
    img_width_max_px = 4000
    img_height_max_px = 3000
    img_width_cropped = 4000
    img_height_cropped = 3000  # note, this was cropped to 2250 in Ricardo's test images
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
        row["relative_altitude"],
        radians(row["yaw"]),
        radians(row["roll"]),
        radians(row["pitch"]),
        row["centroid_x_utm"],
        row["centroid_y_utm"]
    ), axis=1)

    # unpack the vector into a polygon
    exif_df["bbox_poly_geom"] = exif_df.apply(lambda row: unpack_bbox(row["bbox_vec"]), axis=1)

    return exif_df


if __name__ == "__main__":

    # Test this out with by first converting a .jpg to bytes, then calling get_exif() on the bytes
    with open('Basalt_4_HOLDOUT_SET/DJI_0459.JPG', 'rb') as image_file:
        image_in_bytes = image_file.read()

    print(get_exif(image_in_bytes))
