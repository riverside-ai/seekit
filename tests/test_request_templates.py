from seekit import get_provider
from seekit.providers._base import HarRequestTemplate


def test_google_request_template_replaces_keyword() -> None:
    template = get_provider("google").get_request_template("Latest OpenAI")

    assert isinstance(template, HarRequestTemplate)
    assert template.method == "GET"
    assert "Latest%20OpenAI" in template.url or "Latest+OpenAI" in template.url
    assert all(not name.startswith(":") for name, _ in template.headers)


def test_threads_request_template_replaces_keyword_in_body() -> None:
    template = get_provider("threads").get_request_template("fresh keyword")

    assert template.method == "POST"
    assert template.body is not None
    assert "fresh keyword" in template.body or "fresh+keyword" in template.body
