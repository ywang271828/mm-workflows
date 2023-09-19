#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: DiffDock Diffusion pose ranking

doc: |-
  DiffDock Diffusion pose ranking

baseCommand: ["python", "/rank_diffdock_poses.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/rank_diffdock_poses

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
   listing:
     - entry: $(inputs.output_files_path)

inputs:

  output_files_path:
    type: Directory

  top_n_confident:
    type: float
    inputBinding:
      prefix: --top_n_confident
    default: 10

  top_percent_confidence:
    type: float
    inputBinding:
      prefix: --top_percent_confidence
    default: 33

  output_poses:
    type: string?


outputs:

  output_poses:
    type:
      type: array
      items: File
    outputBinding:
      glob: "*ranked*.sdf"
    format: edam:format_3814

  stdout:
    type: File
    outputBinding:
      glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl