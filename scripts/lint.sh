poetry update
poetry run isort .
poetry run black .
poetry run flake8 . --statistics
poetry run bandit --recursive . -c pyproject.toml 