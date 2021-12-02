
**Example usage of how to generate the final UI**

0.) First import the dependencies
```
from georeference_from_byte import get_exif
from map_ui import build_map
```

1.) Extract the necessary georeferenced data from an UNANNOTATED image in memory (which should contain exif and xml positioning data)
```
single_row_df = get_exif(image_in_bytes)
```
2.) Join in the yolov5 cow count

```
single_row_df["cow_count"] = 5
```

3.) Keep appending to a global dataframe as the images stream in and then call the build_map() bethod from map_ui.py

```
build_map(global_df, img_dir="Basalt_4_HOLDOUT_SET/")
```
(Note the img_dir should be the public s3 bucket http:// string where we are writing the ANNOTATED images to. All images should be made public as well.)
