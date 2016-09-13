# Simple makefile for quality

ifeq ($(OS),Windows_NT)
	NOSE=nosetests
else
	NOSE=nosetests3
endif

test:
	@echo "Running tests..."
	PYTHONPATH=. $(NOSE) -v
	@echo "Done."
	
cov:
	@echo "Coverage..."
	@$(NOSE) -v --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-branches --cover-html
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265,E501
	@echo "Done."



check: cov pep8
