from seekit import get_provider
from har import load_engine_configs
from seekit.providers._base import RequestTemplate


def test_google_request_template_replaces_keyword() -> None:
    template = get_provider("google").get_request_template("Latest OpenAI")

    assert isinstance(template, RequestTemplate)
    assert template.method == "GET"
    assert "Latest%20OpenAI" in template.url or "Latest+OpenAI" in template.url
    assert all(not name.startswith(":") for name in template.headers)


def test_threads_request_template_replaces_keyword_in_body() -> None:
    template = get_provider("threads").get_request_template("fresh keyword")

    assert template.method == "POST"
    assert template.body is not None
    assert "fresh keyword" in template.body or "fresh+keyword" in template.body


def test_keyword_replacement_updates_header_values() -> None:
    template = get_provider("tiktok").get_request_template("fresh keyword")

    assert "OpenClaw" not in template.headers["referer"]
    assert "fresh keyword" in template.headers["referer"] or "fresh+keyword" in template.headers["referer"]


def test_dev_engine_config_loads_from_repo_data() -> None:
    configs = load_engine_configs()

    assert configs
    assert any(config.name == "google" for config in configs)
