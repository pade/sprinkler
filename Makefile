# Simple makefile for quality

PYTEST=pytest

test: unit long_test functional

unit:
	@echo "Running unit tests..."
	$(PYTEST) -v -m 'not longtest and not functional' --ignore=sprinkler-env
	@echo "Done."

long_test:
	@echo "Running long tests..."
	$(PYTEST) -v -m 'longtest' --ignore=sprinkler-env
	@echo "Done."

functional:
	@echo "Running functional tests..."
	$(PYTEST) -v -m 'functional' --ignore=sprinkler-env
	@echo "Done."

cov:
	@echo "Coverage..."
	$(PYTEST) -v --cov-report html --cov  --ignore=sprinkler-env
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="sprinkler-env,docs,test*" --max-line-length=90 --ignore=E127,E265,E501
	@echo "Done."



check: test pep8
