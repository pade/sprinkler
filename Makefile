# Simple makefile for quality

test:
	@echo "Running tests..."
	PYTHONPATH=. nosetests3 -v
	@echo "Done."
	
cov:
	@echo "Coverage..."
	@nosetests3 -v --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-branches --cover-html
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265
	@echo "Done."



check: cov pep8
