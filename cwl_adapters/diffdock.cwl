#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: DiffDock Diffusion based protein ligand docking

doc: |-
  DiffDock Diffusion based protein ligand docking

baseCommand: ["bash", "diffdock_cmds.sh"]

hints:
  DockerRequirement:
    dockerPull: mrbrandonwalker/diffdock_cpu

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing: |
      ${
        var lst = [];
        lst.push(inputs.protein_path);
        lst.push(inputs.ligand_path);
        lst.push(inputs.script_path);
        return lst;
      }

inputs:

  script_path:
    type: File

  protein_path:
    type: File

  ligand_path:
    type: File

  protein_ligand_inputs:
    label: csv file of protein and ligand file paths
    type: File
    inputBinding:
      prefix: --protein_ligand_csv

  inference_steps:
    label: number of reverse diffusion steps
    type: int?
    inputBinding:
      prefix: --inference_steps
    default: 20

  samples_per_complex:
    label: Number of sample poses to generate per complex
    type: int?
    inputBinding:
      prefix: --samples_per_complex
    default: 40

  batch_size:
    label: input batch size for neural net
    type: int?
    inputBinding:
      prefix: --batch_size
    default: 10

  out_dir:
    label: where output from diffdock is saved
    type: string?
    inputBinding:
      prefix: --out_dir
    default: results/

  model_dir:
    label: directory of DiffDock score model from paper
    type: string?
    inputBinding:
      prefix: --model_dir
    default:  /DiffDock/workdir/paper_score_model/

  confidence_model_dir:
    label: directory of DiffDock confidence model from paper
    type: string?
    inputBinding:
      prefix: --confidence_model_dir
    default:  /DiffDock/workdir/paper_confidence_model

  output_files:
    type: string?

  execution_time:
    type: string?

outputs:

  output_files:
    type: Directory?
    outputBinding:
      glob: $(inputs.out_dir)

  stdout:
    type: File
    outputBinding:
      glob: stdout

  stderr:
    type: File
    outputBinding:
      glob: stderr

  execution_time:
    label: Time to run DiffDock
    doc: |-
      Time to run DiffDock
    type: float
    outputBinding:
      glob: stderr
      loadContents: true
      outputEval: |
        ${
          // the time command outputs to stderr and not to stdout
          // example output below, parse the float value of seconds (first item in line)
          // 345.6
          const lines = self[0].contents.split("\n");
          for (var i = 0; i < lines.length; i++) {
            const indices = lines[i].split(" ");
            if (indices.length == 1) {
              if (indices[0] != '') {
                  const datum = parseFloat(indices[0]);
                  return datum;
              }
            }
          }
        }

stdout: stdout

stderr: stderr

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl