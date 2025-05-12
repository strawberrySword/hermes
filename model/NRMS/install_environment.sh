#!/usr/bin/env bash -i


conda create -n recSys python=3.9

conda activate recSys


pip install recommenders
pip install --upgrade tensorflow==2.15.0

python -m ipykernel install --user --name recSys --display-name recSys_kernel
