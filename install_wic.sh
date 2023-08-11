#!/bin/bash -e

###
# 1. Can't have cyclic dependencies in Git Submodules.
# 2. In setup.cfg, using 
#    `
#    install_requires =
#        wic[all] @ git+https://github.com/PolusAI/workflow-inference-compiler.git
#    `
#    downloads and installs pip dependencies before the mamba system dependencies.
# 3. Temporarily solution here is to manually clone the WIC repository, and then run the mamba
#    system dependency installation first before running the pip dependency installation.
###
rm -rf workflow-inference-compiler &> /dev/null


git clone https://github.com/PolusAI/workflow-inference-compiler.git
cd workflow-inference-compiler
./install_system_deps.sh
pip install -e ".[all]"
cd ..