import click
from typeahead import app
from typeahead.index import SearchIndex
from typeahead.counter import WordCounter


@app.cli.command("word_count")
@click.argument("input_path")
@click.argument("output_path")
def word_count(input_path, output_path):
    wordCounter = WordCounter()
    wordCounter.update(input_path)
    wordCounter.save(output_path)


@app.cli.command("index")
@click.argument("input_path")
@click.argument("output_dir")
@click.argument("version")
def index(input_path, output_dir, version):
    max_prefix_size = app.config.get("MAX_PREFIX_SIZE")
    max_heap_size = app.config.get("MAX_HEAP_SIZE")

    searchIndex = SearchIndex(max_heap_size,max_prefix_size)
    searchIndex.make_index(input_path)
    searchIndex.save(output_dir, version=version)
