# Exif extraction dependencies
import re
import io
from PIL import Image, ExifTags  # should be pip install pillow
import pandas as pd

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


def gps_dms_to_dd(image_dms):
    """
    Quick and dirty function to convert exif lat long in dms to dd
    :param image: the image stored as bytes
    :return: (lat, long) tuple
    """
    degrees = float(image_dms[0])
    minutes = float(image_dms[1])
    seconds = float(image_dms[2])
    dd = degrees + minutes / 60 + seconds / 3600

    return dd


def get_exif(image_bytes):
    """
    :param image_bytes: image variable stored as bytes
    :return: Single-row dataframe that can be appended to a blank global dataframe used to populate html map
    """
    # Convert bytes to image object using exif module
    image = Image.open(io.BytesIO(image_bytes))

    # Grab the core exif information
    exif_dict = {
        ExifTags.TAGS[k]: v
        for k, v in image._getexif().items()
        if k in ExifTags.TAGS
    }

    # Grab the additional DJI-specific xml for additional sensor detail
    xmldata = image.__dict__['app']
    xml_string = xmldata["APP1"].decode("utf-8").lower()
    data_list = re.findall('dji\:(.*?)\\n', xml_string)
    data_list = [string.split("=") for string in data_list]
    sensor_dict = {i[0]: i[1] for i in data_list}

    for k, v in sensor_dict.items():
        sensor_dict[k] = float(v.strip('"'))  # convert string of string into float

    # Blank dataframe for storing exif and geo data
    exif_df = pd.DataFrame()

    # Details from the image's core exif data
    exif_df["filename"] = [exif_dict["ImageDescription"][14:]]  # just pull out "DJI_XXXX.JPG"
    exif_df["lat_dd"] = gps_dms_to_dd(exif_dict["GPSInfo"][2])
    exif_df["long_dd"] = -1 * gps_dms_to_dd(exif_dict["GPSInfo"][4])  # negative longitude

    # Sensor details from the DJI's xml data
    exif_df["pitch"] = float(sensor_dict["gimbalpitchdegree"])
    exif_df["yaw"] = float(sensor_dict["gimbalyawdegree"])
    exif_df["roll"] = float(sensor_dict["gimbalrolldegree"])
    exif_df["relative_altitude"] = float(sensor_dict["relativealtitude"])

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
    img_width_cropped = float(exif_dict["ExifImageWidth"])
    img_height_cropped = float(exif_dict["ExifImageHeight"])  # this was cropped to 2250 in Ricardo's test images
    sensor_width_mm = 6.3  # not contained in exif
    sensor_height_mm = 4.7  # not contained in exif
    focal_length = float(exif_dict["FocalLength"])

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