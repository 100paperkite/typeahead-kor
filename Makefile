.PHONY: requirements clean

clean:
	find . -type f -name '*.pyc' -delete

requirements:
	pip3 install -r requirements.txt

