#!/bin/bash -e
TIMEFORMAT=%R && time python /DiffDock/inference.py "$@"
# need to remove large files otherwise cachedir folder will be 3GB each!!
rm .*.npy
rm -r .cache/