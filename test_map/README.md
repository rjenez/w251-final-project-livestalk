
**Example usage of how to generate the final UI (reading drone images in bytes rather than from .jpg file)**

0. Import the dependencies
```
import pandas as pd
from georeference_from_byte import get_exif
from map_ui import build_map
```

1. Extract the necessary georeferenced data from an UNANNOTATED image in memory (which should contain exif and xml positioning data)
```
single_row_df = get_exif(image_in_bytes)
```
2. Join in the yolov5 cow count

```
single_row_df["cow_count"] = 5
```

3. Keep appending to a global dataframe as the images stream in and then call the build_map() method from map_ui.py

```
build_map(global_df, img_dir="Basalt_4_HOLDOUT_SET/")
```

This will write out livestalk_map.html (the final UI) in the current working directory, which I think should be an s3 bucket which allows for web hosting.
(Note the img_dir should be the public s3 bucket http:// string where we are writing the ANNOTATED images to. This will generate a hyperlink within the map tooltip to the annotated image. All images should be made public as well.).

Jeff's script should keep calling build_map() in the listening loop so we can keep refreshing the .html file for "real-time" UI.

**Methodology Details**

We estimated each drone image's geographic frame of reference by following the calculations in this stack overflow post:
https://stackoverflow.com/questions/38099915/calculating-coordinates-of-an-oblique-aerial-image

We took the yaw, pitch, and roll of the sensor as well as the drone camera's vertical and horizontal field of view to calculate four rays of each image and the points at which the rays intersected the ground. All inputs needed to be converted from degrees into radians. For latitude and longitude of the drone, we needed to convert such coordinates into Easting and Northing coordinates (cartesian coordinates represented in meters relative to some axis). We modified a Python script which calculated the ray intersection offsets to account for the actual position of the drone. We also had to project the final bounding boxes into the correct local projection (Basalt, CO) for proper rendering.
