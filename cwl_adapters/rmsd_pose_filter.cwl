#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: RMSD for crystal vs predicted poses

doc: |-
  RMSD for crystal vs predicted poses

baseCommand: ["python", "/rmsd_poses.py"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/rmsd_poses

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing: |
      ${
        const lst = [];
        for (var i = 0; i < inputs.predicted_poses.length; i++) {
          lst.push(inputs.predicted_poses[i]);
        }
        lst.push(inputs.crystal_pose_path);
        return lst;
      }

inputs:

  centroid_cutoff:
    type: float
    default: 5
    inputBinding:
      prefix: --centroid_cutoff

  input_json_name:
    type: string
    default: "output.json"
    format:
    - edam:format_3816
    inputBinding:
      prefix: --output_json_name

  predicted_poses:
    type:
      type: array
      items: File
    inputBinding:
      itemSeparator: ","
      separate: false
      prefix: --predicted_poses=

  crystal_pose_path:
    type: File
    format:
    - edam:format_3814
    inputBinding:
      prefix: --crystal_pose_path

  use_clustering_filter:
    type: boolean
    inputBinding:
      prefix: --use_clustering_filter

  rmsd_json:
    type: string?

  filtered_poses:
    type: string?

outputs:

  rmsd_json:
    type: File
    outputBinding:
      glob: $(inputs.input_json_name)

  filtered_poses:
    type: File[]
    outputBinding:
      glob: "*filtered*.mol"

  stdout:
   type: File
   outputBinding:
     glob: stdout

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl