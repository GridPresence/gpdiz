MODULE := gpdiz
IGOR_DEPLOY_RELEASE ?= --no-rel
IGOR_PATCH_LEVEL ?= patch
UPVERSION := $(shell igor pkg vnum-plus ${MODULE} ${IGOR_PATCH_LEVEL} ${IGOR_DEPLOY_RELEASE})
PARALLEL := $(shell nproc)

.PHONY: report
report:
	@igor --version
	@echo "Upgrade version to ${UPVERSION}"

.PHONY: test
test:
	@python3 -m pytest

.PHONY: lint
lint:
	@python3 -m pylint -j ${PARALLEL} ${MODULE}/

.PHONY: typehint
typehint:
	@python3 -m mypy --ignore-missing-imports --check-untyped-defs ${MODULE}

.PHONY: format
format:
	@python3 -m black ${MODULE}/*.py

.PHONY: check
check: report format lint typehint test

.PHONY: clean
clean:
	@rm -fr dist .mypy_cache .pytest_cache ${IGOR_BUILD}/${MODULE}

.PHONY: deploy
deploy: check clean
	@igor iam whoami ${IGOR_CA_DOM_OWN}
	@tbump --non-interactive --only-patch ${UPVERSION}
	@python3 -m build --no-isolation --outdir ${IGOR_BUILD}/${MODULE}/dist
	@python3 -m twine upload --cert ${JFCA} -r local ${IGOR_BUILD}/${MODULE}/dist/* --verbose
	@aws codeartifact login --tool twine --repository ${IGOR_CA_DOM_REP} --domain ${IGOR_CA_DOM} --domain-owner ${IGOR_CA_DOM_OWN}  --region ${IGOR_CA_DOM_REG}
	@python3 -m twine upload -r codeartifact ${IGOR_BUILD}/${MODULE}/dist/* --verbose