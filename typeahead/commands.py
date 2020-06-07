import click
from typeahead import app
from typeahead.index import SearchIndex
from typeahead.word_counter import WordCounter


@app.cli.command("word_count")
@click.argument("input_path")
@click.argument("output_path")
def word_count(input_path, output_path):
    wordCounter = WordCounter()
    wordCounter.update(input_path)
    wordCounter.save(output_path)


@app.cli.command("index")
@click.argument("input_path")
@click.argument("output_path")
@click.argument("max_prefix_size")
@click.argument("max_heap_size")
def index(input_path, output_path, max_prefix_size, max_heap_size):
    searchIndex = SearchIndex()
    searchIndex.make_index(input_path=input_path,
                           max_prefix_size=int(max_prefix_size),
                           max_heap_size=int(max_heap_size))
    searchIndex.save(output_path)
