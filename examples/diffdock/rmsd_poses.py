# pylint: disable=E1101,E0401
"""Cluster predicted diffdock poses by centroid, \
    keep most confident from each cluster then compute RMSD to crystal pose"""
# gmx_rms_nofit.cwl only used for gromacs trajectory file so need way to compute
# RMSD from mol files

import argparse
import json
from pathlib import Path
import shutil
from typing import Dict
import re

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolTransforms as rdmt
from rdkit.ML.Cluster import Butina
from openbabel import openbabel
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--predicted_poses', help='List of predicted pose files')
parser.add_argument('--crystal_pose_path', type=str, help='Crystal pose file path')
parser.add_argument('--output_json_name', type=str, help='Output json file')
parser.add_argument('--centroid_cutoff', type=float,
                    help='RMSD cutoff for clusters of poses in same protein pocket')
parser.add_argument('--use_clustering_filter', dest='use_clustering_filter',
                    action='store_true', help='')
parser.set_defaults(use_clustering_filter=False)
args = parser.parse_args()
args.crystal_pose_path = Path(args.crystal_pose_path).name

# strip file path and just keep filenames
SKIP = True
if args.predicted_poses is not None:
    SKIP = False
    obConversion = openbabel.OBConversion()
    obConversion.SetInFormat('sdf')
    obConversion.SetOutFormat('mol')
    predicted_poses = args.predicted_poses.split(',')
    predicted_poses = [Path(i).name for i in predicted_poses]
    poses = []
    for pred_pose in predicted_poses:
        ligmol = openbabel.OBMol()
        obConversion.ReadFile(ligmol, pred_pose)
        molname = pred_pose.replace('.sdf', '.mol')
        obConversion.WriteFile(ligmol, molname)
        poses.append(molname)
    pred_mols = [Chem.MolFromMolFile(i) for i in poses]
    if None in pred_mols:  # unreproducible failure rdkit returned None in virtual screen
        SKIP = True


def return_json_file(input_dict: Dict, output_file: str) -> None:
    """This function returns a json file from an input dictionary

    Args:
        input_dict (Dict): Input dictionary to be saved as a json file
        output_file (str): Name of json file to be saved
    """
    with open(output_file, "w", encoding='UTF-8') as outfile:
        json.dump(input_dict, outfile, indent=2)


def parse_confidence(file_name: str) -> float:
    """This function return confidence score from filename

    Args:
        file_name (str): The filename of output pose

    Returns:
        float: The confidence value from pose
    """
    confidence = float(re.findall('rank[0-9]*[0-9]_confidence(.*).mol', file_name)[0])
    return confidence


output: Dict = {}

if SKIP is False:
    # Compute centroid distance for each pose pair
    index_to_name = {}
    dists = []
    for i, pred_mol in enumerate(pred_mols):
        pred_name = poses[i]
        index_to_name[i] = pred_name
        conf = pred_mol.GetConformers()[0]
        center = rdmt.ComputeCentroid(conf)
        for j in range(i):
            opred_name = poses[j]
            opred_mol = pred_mols[j]
            oconf = opred_mol.GetConformers()[0]
            ocenter = rdmt.ComputeCentroid(oconf)
            dists.append(np.linalg.norm(center-ocenter))

    # Cluster a pose into group of other poses via centroid distance if beneath threshold
    true_poses = []
    clusters = Butina.ClusterData(dists, len(pred_mols), args.centroid_cutoff, isDistData=True)
    for cluster in clusters:
        names = [index_to_name[k] for k in cluster]
        confidences = [parse_confidence(k) for k in names]
        max_confidence = max(confidences)
        confidence_to_name = dict(zip(confidences, names))
        max_name = confidence_to_name[max_confidence]
        new_name = f"filtered_{max_name}"
        # Beware of issues with shutil.copy https://docs.python.org/3/library/shutil.html
        shutil.copy(max_name, new_name)
        true_poses.append(new_name)

    if args.use_clustering_filter is False:
        true_poses = poses[:]

    # Generate rdkit objects for computing RMSD
    ref_mol = Chem.MolFromMolFile(args.crystal_pose_path)
    pred_mols = [Chem.MolFromMolFile(i) for i in true_poses]
    pred_name_to_mol = dict(zip(true_poses, pred_mols))

    # save pose name, RMSD filename to json file
    output_dict: Dict[str, Dict[str, float]] = {}
    for pred_name, pred_mol in pred_name_to_mol.items():
        RMSD = AllChem.GetBestRMS(pred_mol, ref_mol)
        rmsd_dict = {'RMSD': RMSD}
        output_dict = {pred_name: rmsd_dict}
    return_json_file(output_dict, args.output_json_name)
else:
    return_json_file(output, args.output_json_name)
