`seekit` is a python package that wraps various search engine API into a uniform interface.


## TODO

Once you finished one task, check the box. Work on the task ONE BY ONE.

### Initial

- [x] Design the common interface for a search response item. At least including:
    - title
    - excerpt
    - url
    Use pydantic to create this model
- [x] Load the ./data/info.yaml, which contains the sites we want to support.
    Each site's search response page is stored in an HAR file, the response
    content is base64 encoded, so you need to use a tool to parse it.
    Create a base class in `./seekit/providers/_base.py`, create each class in corresponding
    python files. 
    You need to iterate over the sites one by one, do NOT read them all,
    otherwise you context window will be full.
    For HTML, preferably use xpath or css expression to extract each row, and
    then extract each item. For JSONP, first convert them to JSON.
- [x] Update the readme and generate AGENTS.md
- [x] Generate unittest against the HAR files

### Polish

- [x] Add `provider`, and optional `author` and `cover_url` to the SerpItem
- [x] Generate skills so that this package can be Codex/ClaudeCode/OpenClaw,
    Agents will use this package to search the web to find latest info on given words.
- [x] In BaseSERP, add a request method, which use curl_cffi to fetch the page,
    using headers from the HAR file, in exact order. The SERP class should fetch live
    from the web, not parsing HAR files.
- [x] Remove qihoo.py
- [x] Add proper type annotations as much as possible

### Bugfixes

- [x] Remove referencing local files, the package is not working on other machines
- [x] The "OpenClaw" in each request url is a place holder, we need to pass the keyword
    to the request.

### Further

- [x] Add a `--debug` option for the CLI, which raises exceptions and saves the response
    html for debugging
- [x] Add a optional time field in SerpItem
- [x] Provide a dockerfile
- [x] Run as a server to provide API and web page
- [x] Add docs on with readthedocs
- [x] Use python rich to build a nicer CLI interface

### New

- [x] Redesign the CLI, support the following options

    seekit KEYWORD --engine baidu  # search with baidu
    seekit KEYWORD  # direct search using the default bing engine
    seekit KEYWORD --format json  # show result in json
    seekit KEYWORD --format csv  # show result in csv

## Candidates

This part is for future versions, we don't consider these tasks for now.

- [ ] Decode item URLs
