# Exif extraction dependencies
import pandas as pd
import exiftool

# Georeferencing dependencies
from math import degrees, radians, atan
from pyproj import Proj
from camera_calculator import CameraCalculator
from shapely.geometry import Polygon


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
    # Ensure this matches the projection in get_exif()
    pp2 = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    long_list, lat_list = pp2(x_list, y_list, inverse=True)
    bbox_geom = Polygon(zip(long_list, lat_list))
    return bbox_geom


def get_exif(image_path="Basalt_4_HOLDOUT_SET/DJI_0459.JPG"):
    """
    Extracts all the necessary exif data and performs calculations needed for georeferencing the image on map
    12/01: Note, currently this does not read from bytes, but the .jpg image itself
    :param image_path: path to the UNANNOTATED .jpg written to s3
    :return: Single-row dataframe that can be appended to a blank global dataframe used to populate html map
    """
    # Grab the metadata for the image
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(image_path)

    exif_df = pd.DataFrame.from_dict([metadata])  # dict needs to be wrapped in list

    # keep only necessary fields for bbox calculation
    exif_df = exif_df[["File:FileName", "MakerNotes:CameraPitch", "MakerNotes:CameraYaw", "MakerNotes:CameraRoll",
                       "XMP:RelativeAltitude", "EXIF:GPSLatitude", "EXIF:GPSLongitude"]]

    # Make sure altitude is float rather than str
    exif_df["XMP:RelativeAltitude"] = exif_df["XMP:RelativeAltitude"].str[1:].apply(pd.to_numeric)

    # Add negative sign in front of longitude
    exif_df["EXIF:GPSLongitude"] = -1 * exif_df["EXIF:GPSLongitude"]

    # Lat Long conversion from decimal degrees to UTM
    # UTM zone is set for Carbondale, CO (demo flyby location)
    # Use http://rcn.montana.edu/Resources/Converter.aspx to check the right zone
    pp = Proj("+proj=utm +zone=13 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Convert the centroid lat, long to UTM
    c_x_utm, c_y_utm = pp(exif_df["EXIF:GPSLongitude"].values, exif_df["EXIF:GPSLatitude"].values)
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
        row["XMP:RelativeAltitude"],
        radians(row["MakerNotes:CameraYaw"]),
        radians(row["MakerNotes:CameraRoll"]),
        radians(row["MakerNotes:CameraPitch"]),
        row["centroid_x_utm"],
        row["centroid_y_utm"]
    ), axis=1)

    # unpack the vector into a polygon
    exif_df["bbox_poly_geom"] = exif_df.apply(lambda row: unpack_bbox(row["bbox_vec"]), axis=1)

    return exif_df
