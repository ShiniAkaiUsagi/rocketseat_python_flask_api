python.exe -m pip install --upgrade pip
pip install -U poetry
poetry self add poetry-plugin-export
poetry self update
poetry update
poetry run pre-commit run
# Para sessão do vscode
poetry export --without-hashes --format=requirements.txt -o requirements.txt
pip install -U -r requirements.txt
