from pathlib import Path

import pytest

from seekit import PROVIDERS, parse_har
from seekit.providers._base import EngineConfig, load_engine_configs


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("engine", load_engine_configs(ROOT / "data" / "info.yaml"))
def test_engine_fixture_parses(engine: EngineConfig) -> None:
    provider = engine.name
    assert provider in PROVIDERS

    fixture = ROOT / "data" / "pages" / engine.example.page
    items = parse_har(provider, fixture)

    assert items, provider
    assert any(item.title for item in items), provider
    assert any(item.url for item in items), provider
    assert all(item.provider == provider for item in items), provider
