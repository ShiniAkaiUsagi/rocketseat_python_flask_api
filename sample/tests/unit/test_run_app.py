import pytest

from unittest.mock import patch
from sample.src.app import run_app


@pytest.mark.api
class TestRunApp:
    def test_run_app_calls_app_run(self):
        with patch("sample.src.app.app.run") as mock_run:
            run_app()
            mock_run.assert_called_once()
