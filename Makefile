.PHONY: install clean-pyc test run


clean-pyc:
	find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	find . -type d -name "__pycache__" | xargs rm -r

install:
	pip3 install -r requirements.txt

test:
	python -m pytest -n0  --cov-append --cov-report term

run:
	FLASK_APP=./typeahead/app.py flask run -h localhost -p 5000