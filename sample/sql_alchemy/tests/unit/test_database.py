from unittest.mock import MagicMock

import pytest
from flask import Flask

from sample.sql_alchemy.src.database import init_app


@pytest.mark.database
class TestInitApp:
    def test_should_apply_test_config_when_provided(self):
        app = Flask(__name__)
        test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
        init_app(app, test_config=test_config)
        for key, value in test_config.items():
            assert app.config[key] == value

    def test_should_apply_default_config_when_test_config_not_provided(self):
        app = Flask(__name__)
        init_app(app)
        assert (
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "mysql+pymysql://root:123456@localhost:3306/sql_alchemy_db"
        )
        assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False

    def test_should_initialize_db_with_app(self, monkeypatch):
        mock_db = MagicMock()
        app = Flask(__name__)
        monkeypatch.setattr("sample.sql_alchemy.src.database.db", mock_db)
        init_app(app)
        mock_db.init_app.assert_called_once_with(app)
