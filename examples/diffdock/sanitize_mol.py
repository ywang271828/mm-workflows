# pylint: disable=E1101,E0401
"""Get rid of kekulization errors. Assign formal charge based on valence."""
# https://depth-first.com/articles/2020/02/10/a-comprehensive-treatment-of-aromaticity-in-the-smiles-language/
# Beware of issues with shutil.copy https://docs.python.org/3/library/shutil.html
import argparse
from pathlib import Path
import shutil
from typing import Dict

import rdkit
from rdkit import Chem
from openbabel import openbabel

parser = argparse.ArgumentParser()
parser.add_argument('--ligand_path', type=str, help='Ligand file path')
args = parser.parse_args()
ligand = Path(args.ligand_path).name
molname = f"clean_{ligand}"


def adjust_formal_charges(molecule: Chem.SDMolSupplier) -> Chem.SDMolSupplier:
    """Sometimes input structures do not have correct formal charges corresponding
    to bond order topology. So choose to trust bond orders assigned and generate formal
    charges based on that.
    Explicit valence determined what the formal charge should be from dictionary of valence
    to formal charge for that atomic number. Special case if atom == carbon or nitrogen
    and if neighbors contain nitrogen, oyxgen or sulfur (polarizable atoms) then if carbon
    and explicit valence only 3, give formal charge of +1 (more stable then -1 case).

    Args:
        molecule (Chem.SDMolSupplier): The rdkit molecule object

    Returns:
        Chem.SDMolSupplier: Molecule object with adjusted formal charges
    """
    # 1=H, 5=B, 6=C, 7=N, 8=O, 15=P, 16=S, 17=Cl, 9=F, 35=Br, 53=I
    atomicnumtoformalchg: Dict[int, Dict[int, int]] = {1: {2: 1}, 5: {4: 1}, 6: {3: -1}, 7: {2: -1, 4: 1},
                                                       8: {1: -1, 3: 1}, 15: {4: 1}, 16: {1: -1, 3: 1, 5: -1},
                                                       17: {0: -1, 4: 3}, 9: {0: -1}, 35: {0: -1}, 53: {0: -1}}
    for atom in molecule.GetAtoms():
        atomnum = atom.GetAtomicNum()
        val = atom.GetExplicitValence()
        if atomicnumtoformalchg.get(atomnum) is None:
            continue
        valtochg = atomicnumtoformalchg[atomnum]
        chg = valtochg.get(val, 0)
        # special case of polar neighbors surrounding carbon or nitrogen
        # https://docs.eyesopen.com/toolkits/cpp/oechemtk/valence.html
        # https://www.masterorganicchemistry.com/2011/03/11/3-factors-that-stabilize-carbocations/
        polneighb = False
        if atomnum in (6, 7):
            for natom in atom.GetNeighbors():
                natomicnum = natom.GetAtomicNum()
                if natomicnum in (7, 8, 16):
                    polneighb = True
            if polneighb and val == 3 and atomnum == 6:
                chg = 1

        atom.SetFormalCharge(chg)
    return molecule


def babel_remove_aromatic_bonds(molname_ins: str) -> None:
    """Openbabel seems to be able to remove aromatic bonds (shows up as bond order 4 in SDF)
    Need to remove this before rdkit can read the molecule. Openbabel attempts to assign
    a kekule form automatically. Strange cases can happen such as if indole ring nitrogen
    is missing a hydrogen, then the kekule form you would expect for indole ring is not
    assigned and one of the carbons in between both rings will be assigned formal charge of -1
    (since three bonds all single bond order).
    See huckes rule https://www.masterorganicchemistry.com/2012/06/29/huckels-rule-what-does-4n2-mean/

    Args:
        molname_ins (str): The molname of new output SDF file
    """
    ob_conversion = openbabel.OBConversion()
    ob_mol = openbabel.OBMol()
    in_format = ob_conversion.FormatFromExt(molname_ins)
    ob_conversion.SetInFormat(in_format)
    ob_conversion.ReadFile(ob_mol, molname_ins)
    ob_conversion.SetOutFormat(in_format)
    ob_conversion.WriteFile(ob_mol, molname_ins)


def sanitize_mol(molecule: Chem.SDMolSupplier, molname_ins: str) -> None:
    """Call adjust_formal_charges to ensure that formal charges are consistent with bond orders.

    Args:
        molecule (Chem.SDMolSupplier): The rdkit molecule object
        molname_ins (str): The molname of new output SDF file
    """
    molecule = adjust_formal_charges(molecule)
    with Chem.SDWriter(molname_ins) as w:
        w.write(molecule)


reader = Chem.SDMolSupplier(ligand, sanitize=False, removeHs=False)
mol: Chem.SDMolSupplier = reader[0]

try:
    Chem.SanitizeMol(mol)
    # can also be explicit valence error (i.e.) formal charge not consistent with bond topology
    # choose to trust bond topology around atom and add formal charge based on that
    shutil.copy(ligand, molname)
except rdkit.Chem.rdchem.KekulizeException as e:
    babel_remove_aromatic_bonds(ligand)
    reader = Chem.SDMolSupplier(ligand, sanitize=False, removeHs=False)
    new_mol: Chem.SDMolSupplier = reader[0]
    sanitize_mol(new_mol, molname)
except rdkit.Chem.rdchem.MolSanitizeException as e:
    sanitize_mol(mol, molname)
