.PHONY: install clean test run index word_count venv


PYTHON=python3
PROJ=typeahead-kor
VENV_PATH = $$HOME/.virtualenvs/${PROJ}

all: clean venv install test

venv:
	$(PYTHON) -m venv $(VENV_PATH) --clear

install:
	pip install -r requirements.txt

test:
	TYPEAHEAD_SETTINGS=config/config-test.py \
	FLASK_APP=./typeahead/app.py \
	$(PYTHON) -m pytest -n0  --cov-append --cov-report term

run:
	FLASK_APP=./typeahead/app.py \
	flask run -h localhost -p $(PORT)

word_count:
	FLASK_APP=./typeahead/commands.py \
	$(PYTHON) -m flask word_count $(input_path) $(output_path)

index:
	FLASK_APP=./typeahead/commands.py \
	$(PYTHON) -m flask index $(input_path) $(output_path) $(max_heap_size) $(max_prefix_size)

clean:
	find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	find . -type d -name "__pycache__" | xargs rm -r