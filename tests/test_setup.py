import argparse
import sys
import time
from typing import Dict
from unittest.mock import patch

from hypothesis.strategies import SearchStrategy
import hypothesis_jsonschema as hj

import wic
import wic.cli
import wic.plugins
import wic.schemas
import wic.schemas.wic_schema
import wic.utils
from wic.wic_types import Json, Yaml


def get_args(yaml_path: str = '') -> argparse.Namespace:
    """This is used to get mock command line arguments.

    Returns:
        argparse.Namespace: The mocked command line arguments
    """
    testargs = ['wic', '--yaml', yaml_path, '--cwl_output_intermediate_files', 'True']  # ignore --yaml
    # For now, we need to enable --cwl_output_intermediate_files. See comment in compiler.py
    with patch.object(sys, 'argv', testargs):
        args: argparse.Namespace = wic.cli.parser.parse_args()
    return args


tools_cwl = wic.plugins.get_tools_cwl(get_args().cwl_dirs_file)
yml_paths = wic.plugins.get_yml_paths(get_args().yml_dirs_file)
yaml_stems = wic.utils.flatten([list(p) for p in yml_paths.values()])
schema_store: Dict[str, Json] = {}
validator = wic.schemas.wic_schema.get_validator(tools_cwl, yaml_stems, schema_store, write_to_disk=True)

yml_paths_tuples = [(yml_path_str, yml_path)
                    for yml_namespace, yml_paths_dict in yml_paths.items()
                    for yml_path_str, yml_path in yml_paths_dict.items()]

for yml_path_str, yml_path in yml_paths_tuples:
    schema = wic.schemas.wic_schema.compile_workflow_generate_schema(yml_path_str, yml_path,
                                                                     tools_cwl, yml_paths, validator)
    # overwrite placeholders in schema_store. See comment in get_validator()
    schema_store[schema['$id']] = schema

validator = wic.schemas.wic_schema.get_validator(tools_cwl, yaml_stems, schema_store, write_to_disk=True)
