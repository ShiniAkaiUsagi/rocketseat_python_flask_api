poetry update
poetry run isort .
poetry run black . 
poetry run flake8 . 
poetry run bandit --recursive .