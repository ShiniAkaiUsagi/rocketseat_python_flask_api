poetry run python -B -m pytest --cache-clear
find . -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
find . -name "*.xml" -delete
find . -name "*.html" -delete

poetry update
poetry run isort .
poetry run black .
poetry run flake8 . --statistics
poetry run bandit --recursive . -c pyproject.toml