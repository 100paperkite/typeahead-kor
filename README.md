# typeahead-kor

API for Autocomplete system

## Set Up
~~~
make clean
~~~
~~~
# virtual environment
make venv
workon typeahead-kor
~~~
~~~
make install
~~~

## Make word count
~~~sh
make word_count input_path=[INPUT_DATA_FILE] output_path=[OUTPUT_WORDCOUNT_FILE]
~~~

## Make index
~~~sh
make word_count input_path=[INPUT_DATA_FILE] output_path=[OUTPUT_WORDCOUNT_FILE] \
                  max_prefix_size=[PREFIX_SIZE] max_heap_size=[HEAP_SIZE]
~~~

## Run
~~~sh
make run PORT=[PORT_NUM]
~~~
