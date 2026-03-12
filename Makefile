UV ?= uv

.PHONY: clean build publish-testpypi publish-pypi upload-testpypi upload-pypi

clean:
	rm -rf build dist src/*.egg-info

build: clean
	$(UV) build

publish-testpypi: build
	uvx uv-publish --publish-url https://test.pypi.org/legacy/ dist/*

publish: build
	uvx uv-publish dist/*

upload-testpypi: publish-testpypi

upload: publish
