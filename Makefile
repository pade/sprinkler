# Simple makefile for quality

PYTEST=pytest

test:
	@echo "Running tests..."
	$(PYTEST) -m 'not longtest'
	@echo "Done."
	
long_test:
	@echo "Running long tests..."
	$(PYTEST) -m 'longtest'
	@echo "Done."
cov:
	@echo "Coverage..."
	$(PYTEST) --cov-report html --cov 
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265,E501
	@echo "Done."



check: cov pep8
