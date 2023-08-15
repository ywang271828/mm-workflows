
#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: This class implements setting up benchmarking inputs for DiffDock

doc: |-
  This class implements setting up benchmarking inputs for DiffDock

baseCommand: "true"
requirements:
  InlineJavascriptRequirement: {}

inputs:

  use_clustering_filter:
    type: boolean?

  use_clustering_filter_out:
    type: string?

  centroid_cutoff:
    type: float

  centroid_cutoff_out:
    type: string?

  protein_path_array:
    type:
      type: array
      items: File
    format:
      - edam:format_1476

  ligand_path_array:
    type:
      type: array
      items: File
    format:
      - edam:format_3814

  samples_per_complex:
    type: int

  inference_steps:
    type: int

  samples_per_complex_out:
    type: string?

  inference_steps_out:
    type: string?

  protein_path_out:
    type: string?

  ligand_path:
    type: string?

  batch_size:
    type: int?

  batch_size_out:
    type: string?

  top_n_confident:
    type: float?

  top_n_confident_out:
    type: string?

  top_percent_confidence:
    type: float?

  top_percent_confidence_out:
    type: string?

outputs:

  use_clustering_filter_out:
    label: use_clustering_filter
    doc: |-
      use_clustering_filter
    type: boolean
    outputBinding:
      outputEval: $(inputs.use_clustering_filter)

  centroid_cutoff_out:
    label: centroid_cutoff
    doc: |-
      centroid_cutoff
    type: float
    outputBinding:
      outputEval: $(inputs.centroid_cutoff)

  samples_per_complex_out:
    label: samples_per_complex
    doc: |-
      samples_per_complex
    type: int
    outputBinding:
      outputEval: $(inputs.samples_per_complex)

  inference_steps_out:
    label: inference_steps
    doc: |-
      inference_steps
    type: int
    outputBinding:
      outputEval: |
        $(inputs.inference_steps)

  protein_path_out:
    label: protein_path
    doc: |-
      protein_path
    type:
      type: array
      items: File
    outputBinding:
      outputEval: $(inputs.protein_path_array)
    format: edam:format_1476

  ligand_path:
    label: ligand_path
    doc: |-
      ligand_path
    type:
      type: array
      items: File
    outputBinding:
      outputEval: $(inputs.ligand_path_array)
    format: edam:format_3814

  batch_size_out:
    label: batch_size
    doc: |-
      batch_size
    type: int
    outputBinding:
      outputEval: $(inputs.batch_size)

  top_n_confident_out:
    label: top_n_confident
    doc: |-
      top_n_confident
    type: float
    outputBinding:
      outputEval: $(inputs.top_n_confident)

  top_percent_confidence_out:
    label: top_percent_confidence
    doc: |-
      top_percent_confidence
    type: float
    outputBinding:
      outputEval: $(inputs.top_percent_confidence)

stdout: stdout

$namespaces:
  edam: https://edamontology.org/