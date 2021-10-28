#!/bin/sh
#Run this after running the notebook to download data from Roboflow
#create folder structure
#all data will be put into 'livestalk-data'
mkdir livestalk-data
mkdir livestalk-data/train
mkdir livestalk-data/train/images
mkdir livestalk-data/train/labels
mkdir livestalk-data/valid
mkdir livestalk-data/valid/images
mkdir livestalk-data/valid/labels
echo new directories created
#create the new data.yaml
cat <<EOF >> livestalk-data/data.yaml
names:
- cow
nc: 1
train: livestalk-data/train/images
val: livestalk-data/valid/images
EOF

# (!!) add more versions here as  we label them (!!)
for version in livestalk-1 livestalk-2 livestalk-3
do
  echo moving data from $version to livestalk-data
  mv -n $version/train/images/* livestalk-data/train/images/
  mv -n $version/train/labels/* livestalk-data/train/labels/
  mv -n $version/valid/images/* livestalk-data/valid/images/
  mv -n $version/valid/labels/* livestalk-data/valid/labels/
  #rm -r $version
done
echo all versions combined into livestalk-data
ls livestalk-data/train/images | echo "There are $(wc -l) files in the consolidated training dir"
ls livestalk-data/valid/images | echo "There are $(wc -l) files in the consolidated validation dir"
