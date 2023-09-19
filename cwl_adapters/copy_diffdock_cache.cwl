#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Copy cache file from container
# note that
# `cp -r inputs.cache_path/. runtime.outdir`
# is equivalent to
# `rsync -r inputs.cache_path runtime.outdir`
# need the /. included in the inputs.cache_path for cp -r to work and then glob the cached files
baseCommand: cp
arguments: ["-r", $(inputs.cache_path), $(runtime.outdir)]

requirements:
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: mrbrandonwalker/diffdock_cpu

inputs:

  cache_path:
    type: string?
    default: "/DiffDock/."

  cache:
    type: string?

outputs:

  cache:
    type:
      type: array
      items: File
    outputBinding:
      glob: ".*npy"

stdout: stdout

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl