# Simple makefile for quality

.DEFAULT_GOAL := help

TEST_SCRIPT = ./src/test/runner.py

test:
	@echo "Running unit tests..."
	@coverage run $(TEST_SCRIPT)
	@echo "Done."

cov: test
	@echo "Coverage..."
	@coverage report
	@coverage html
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pycodestyle . --exclude="docs,test*" --max-line-length=90
	@echo "Done."

autopep8:
	@echo "Applying PEP8 coding style..."
	@autopep8 -iva src/*.py
	@echo "Done."

clean:
	@echo "Cleaning project..."
	@rm -rf htmlcov .coverage
	@echo "Done."

help:
	@echo "\nAvailable commands:"
	@echo "\t-test: Running unit tests"
	@echo "\t-cov: Make coverage report"
	@echo "\t-pep8: Checking PEP8 coding style"
	@echo "\t-clean: Clean project"
	@echo "\t-autopep8: Applying PEP8 (code is modified...)\n"

check: test pep8
