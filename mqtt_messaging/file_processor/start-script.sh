#!/bin/bash
s3fs $S3_BUCKET_NAME $S3_MOUNT_DIRECTORY -o passwd_file=${HOME}/.passwd-s3fs
