"""Generate input table for DiffDock"""
import argparse
import csv
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument('--protein_path', type=str, help='Path to PDB')
parser.add_argument('--ligand_path', type=str, help='Path to ligand file')
parser.add_argument('--output_name', type=str, help='Protein ligand CSV')
args = parser.parse_args()

headers = ["complex_name", "protein_path", "ligand_description", "protein_sequence"]

row = ["", f"./{Path(args.protein_path).name}", f"./{Path(args.ligand_path).name}", ""]

with open(args.output_name, 'w', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerow(row)
