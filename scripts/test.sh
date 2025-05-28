#!/bin/bash

PYTHONPATH=. poetry run pytest
COVERAGE_INDEX_PATH="$(pwd)/htmlcov/index.html"
start "" "$COVERAGE_INDEX_PATH"

echo -e "\n\033[1;34mCobertura gerada! Acesse:\033[0m \033[1;32m$COVERAGE_INDEX_PATH\033[0m\n"