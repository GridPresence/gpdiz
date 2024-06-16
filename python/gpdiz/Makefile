MODULE := gpdiz
BUILD := build

.PHONY: test
test:
	python3 -m pytest

.PHONY: lint
lint:
	python3 -m pylint ${MODULE}/

.PHONY: typehint
typehint:
	python3 -m mypy --ignore-missing-imports --check-untyped-defs ${MODULE}

.PHONY: format
format:
	python3 -m black ${MODULE}/*.py

.PHONY: check
check: format lint typehint test

.PHONY: local
local: check
	python3 -m build --no-isolation --outdir ${BUILD}/${MODULE}/dist
	./local-install