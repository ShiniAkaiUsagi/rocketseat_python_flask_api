#!/bin/bash

python.exe -m pip install --upgrade pip
pip install -U poetry
poetry self update
poetry update
poetry run pre-commit install