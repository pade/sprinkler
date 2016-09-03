# Simple makefile for quality

test:
	@echo "Running tests..."
	PYTHONPATH=. nosetests -v
	@echo "Done."
	
cov:
	@echo "Coverage..."
	@nosetests -v --with-coverage --cover-erase --cover-html-dir=htmlcov --cover-branches --cover-html
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265
	@echo "Done."

check: test cov pep8
