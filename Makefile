# Simple makefile for quality

.DEFAULT_GOAL := help

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
	$(PYTEST) -v --cov-report html --cov
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="sprinkler-env,docs,test*" --max-line-length=90
	@echo "Done."

autopep8:
	@echo "Applying PEP8 coding style..."
	@autopep8 -iva src/*.py
	@echo "Done."

help:
	@echo "\nAvailable commands:"
	@echo "\t-unit: Running unit tests"
	@echo "\t-long_test: Running log duration tests"
	@echo "\t-functional: Running functional tests"
	@echo "\t-cov: Make coverage report"
	@echo "\t-pep8: Checking PEP8 coding style"
	@echo "\t-autopep8: Applying PEP8 (code is modified...)\n"

check: test pep8
