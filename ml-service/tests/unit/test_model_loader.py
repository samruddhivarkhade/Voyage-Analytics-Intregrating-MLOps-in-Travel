import pytest
from pathlib import Path

from app.services.model_loader import load_model, load_encoders


def test_load_model_raises_file_not_found_when_path_missing(monkeypatch, tmp_path):
    from app.core import config
    monkeypatch.setattr(config.settings, "model_path", tmp_path / "no_model.pkl")
    with pytest.raises(FileNotFoundError, match="Model file not found"):
        load_model()


def test_load_encoders_raises_file_not_found_when_path_missing(monkeypatch, tmp_path):
    from app.core import config
    monkeypatch.setattr(config.settings, "encoders_path", tmp_path / "no_encoders.pkl")
    with pytest.raises(FileNotFoundError, match="Encoders file not found"):
        load_encoders()


def test_load_model_error_message_contains_path(monkeypatch, tmp_path):
    from app.core import config
    missing = tmp_path / "some_model.pkl"
    monkeypatch.setattr(config.settings, "model_path", missing)
    with pytest.raises(FileNotFoundError) as exc_info:
        load_model()
    assert str(missing) in str(exc_info.value)


def test_load_encoders_error_message_contains_path(monkeypatch, tmp_path):
    from app.core import config
    missing = tmp_path / "some_encoders.pkl"
    monkeypatch.setattr(config.settings, "encoders_path", missing)
    with pytest.raises(FileNotFoundError) as exc_info:
        load_encoders()
    assert str(missing) in str(exc_info.value)
