#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Prep receptor ligand inputs for DiffDock

doc: |-
  Prep receptor ligand inputs for DiffDock

baseCommand: "true"

requirements:
  InlineJavascriptRequirement: {}

inputs:

  receptor:
    type: File

  ligand:
    type: File

  output_pdb_files:
    type: string?

  output_ligand_files:
    type: string?


outputs:

  output_pdb_files:
    type:
      type: array
      items: File
    outputBinding:
      outputEval: |
        ${
          const lst = [inputs.receptor];
          return lst;
        }
    format: edam:format_1476

  output_ligand_files:
    type:
      type: array
      items: File
    outputBinding:
      outputEval: |
        ${
          const lst = [inputs.ligand];
          return lst;
        }
    format: edam:format_3814

  stdout:
    type: File
    outputBinding:
      glob: stdout


stdout: stdout


$namespaces:
  edam: https://edamontology.org/
  cwltool: http://commonwl.org/cwltool#

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl