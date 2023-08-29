# Simple makefile for quality

.DEFAULT_GOAL := help

UNITTEST = nose2 -v
test: unit

unit:
	@echo "Running unit tests..."
	$(UNITTEST)
	@echo "Done."

cov:
	@echo "Coverage..."
	$(UNITTEST) --with-coverage --coverage-report html --coverage-report term
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pycodestyle . --exclude="docs,test*" --max-line-length=90
	@echo "Done."

autopep8:
	@echo "Applying PEP8 coding style..."
	@autopep8 -iva src/*.py
	@echo "Done."

help:
	@echo "\nAvailable commands:"
	@echo "\t-unit: Running unit tests"
	@echo "\t-cov: Make coverage report"
	@echo "\t-pep8: Checking PEP8 coding style"
	@echo "\t-autopep8: Applying PEP8 (code is modified...)\n"

check: test pep8
