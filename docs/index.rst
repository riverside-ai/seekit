seekit
======

`seekit` provides a unified Python API, CLI, and web server for multiple search providers.

Install
-------

.. code-block:: bash

   uv add seekit

CLI
---

.. code-block:: bash

   seekit google OpenAI --limit 5
   seekit tiktok OpenAI --debug

Python API
----------

.. code-block:: python

   import seekit

   items = seekit.search("OpenAI", provider="google")

Server
------

.. code-block:: bash

   uv run uvicorn seekit.server:app --reload

Endpoints:

- ``GET /api/search?q=OpenAI&provider=google``
- ``GET /`` for a simple web UI
