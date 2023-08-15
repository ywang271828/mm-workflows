#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Sanitize input molecule

doc: |-
  Sanitize input molecule

baseCommand: ["python", "/sanitize_mol.py"]

hints:
  DockerRequirement:
    dockerPull:  mrbrandonwalker/sanitize_mol

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
    - $(inputs.ligand_path)

inputs:

  ligand_path:
    type: File
    format:
    - edam:format_3814
    inputBinding:
      prefix: --ligand_path

  output_file:
    type: string?

outputs:

  output_file:
    type: File
    format: edam:format_3814
    outputBinding:
      glob: "*clean*"


  stdout:
   type: File
   outputBinding:
     glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl