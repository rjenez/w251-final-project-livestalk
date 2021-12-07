# Training and Evaluating YOLOv5 on Livestalk dataset

The notebooks in this folder can be used to perform the following steps:

1. Pull data from roboflow (**data-download.ipynb**)
2. Split data into train / validation / test sets (**resplit-*.ipynb**)
  * **resplit-baseline.ipynb** - create splits for one dataset
  * **resplit-experiments.ipynb** - create splits for four experiment datasets
3. Perform transformations and augmentations on the data (**augmentations-*.ipynb**)
  * **augmentations-baseline.ipynb** - perform transformations on one dataset
  * **augmentations-experiments.ipynb** - perform transformations on four experiment datasets
4. Train YOLOv5 on the produced dataset and evaluate the results (**yolov5-train-val.ipynb**)

To execute these notebooks from a container, first run the file `dockerbuild_model.sh` to build the image, then run `docker_run.sh` to run the container. Once run, the Jupyter Lab environment should be accessible from http:/localhost:8889/.
