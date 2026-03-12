# Repo Guide

## Overview

- `seekit/providers/_base.py` contains the shared `SerpItem` model, HAR request-template helpers, and parser base classes.
- `seekit/providers/*.py` contains one provider parser per engine.
- `data/info.yaml` is the source of truth for supported engines and fixture filenames.
- `tests/` covers both fixture parsing and HAR-derived live request templating.

## Working Rules

- Add providers one by one from `data/info.yaml`; do not load every HAR into context at once.
- Prefer XPath for HTML fixtures. Use embedded JSON or script extraction only when the page is script-driven.
- Keep provider output normalized to `provider`, `title`, `excerpt`, `url`, optional `author`, and optional `cover_url`.
- Live requests should come from HAR-derived headers/body templates instead of hand-written request code.
- When updating fixtures or providers, update the matching tests in the same change.

## Verification

- Run `pytest` when dependencies are available.
- If the local environment is missing parser dependencies, note that explicitly in your handoff.
