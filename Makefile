# Simple makefile for quality

NOSE=nose2

test:
	@echo "Running tests..."
	PYTHONPATH=. $(NOSE) -v -A '!long_test'
	@echo "Done."
	
long_test:
	@echo "Running long tests..."
	PYTHONPATH=. $(NOSE) -v -A 'long_test'
	@echo "Done."
cov:
	@echo "Coverage..."
	@$(NOSE) -v -A '!long_test' --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-branches --cover-html
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265,E501
	@echo "Done."



check: cov pep8
