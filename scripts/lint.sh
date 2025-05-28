#!/bin/bash

poetry run python -B -m pytest --cache-clear

find . -type d \( \
    -name "__pycache__" -o \
    -name "*.pytest_cache" -o \
    -name "htmlcov" \
\) -exec rm -rf {} +

find . -type f \( \
    -name "*.pyc" -o \
    -name "*.xml" -o \
    -name "*.html" -o \
    -name ".coverage" \
\) -delete

poetry update
poetry run isort .
poetry run black .
poetry run flake8 . --statistics
poetry run bandit --recursive . -c pyproject.toml