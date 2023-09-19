"""Ranks predicted poses from DiffDock via confidence score"""
import argparse
from pathlib import Path
import shutil
import re
import glob
from typing import Dict

parser = argparse.ArgumentParser()

parser.add_argument('--top_n_confident', type=int, help='Top n confident poses')
parser.add_argument('--top_percent_confidence', type=float, help='top confidence percent cutoff')
args = parser.parse_args()
base_dir = Path().absolute()

# Map confidence value to pose for filtering step. Find all files with delimiter
# and add to dictionary.
# filename looks like rank16_confidence-0.99.mol
DELIM = "confidence"
confidence_to_pose: Dict[float, str] = {}
for name in glob.glob('**/*confidence*', recursive=True):
    f = Path(name).name
    confidence = float(re.findall('rank[0-9]*[0-9]_confidence(.*).sdf', f)[0])
    confidence_to_pose[confidence] = name

# First filter by absolute value top_n_confident
sorted_list = sorted(confidence_to_pose.items(), reverse=True)
sorted_pose_list = [v for (k, v) in sorted_list]
poses = sorted_pose_list[:args.top_n_confident]

# Next filter by top percentage of confident poses
num_poses = int(args.top_percent_confidence*.01*len(poses))
poses = poses[:num_poses]

# Find the output predicted poses and then if its in list of ranked poses,
# copy filename to be used in next workflow step
for name in poses:
    file_name = Path(name).name
    final_path = Path(base_dir).joinpath(f"ranked_{file_name}")
    final_path = Path(base_dir).joinpath(f"ranked_{file_name}")
    current_path = Path(name)
    # Beware of issues with shutil.copy https://docs.python.org/3/library/shutil.html
    shutil.copy(current_path, final_path)
