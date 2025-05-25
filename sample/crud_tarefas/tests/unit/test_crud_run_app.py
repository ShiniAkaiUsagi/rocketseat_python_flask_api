from unittest.mock import patch

import pytest

from sample.crud_tarefas.src.app import run_app


@pytest.mark.api
class TestRunApp:
    def test_run_app_calls_app_run(self):
        with patch("sample.crud_tarefas.src.app.app.run") as mock_run:
            run_app()
            mock_run.assert_called_once()
