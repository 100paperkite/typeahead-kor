import os
from flask import request, jsonify, Response
from typeahead import app
from typeahead.index import SearchIndex
from typeahead.utils import get_newest_index_path, write_binary_index_element, decompose_korean

index_dir = app.config.get("INDEX_DIR")
searchIndex = SearchIndex()


@app.before_first_request
def load():
    searchIndex.load(get_newest_index_path(index_dir))


@app.route("/")
def info():
    return searchIndex.info()


@app.route("/search/<prefix>")
def search(prefix):
    return jsonify(searchIndex.search(decompose_korean(prefix)))


@app.route("/healthcheck")
def healthcheck():
    return Response(status=200)


@app.route("/admin/index/reload", methods=["POST"])
def reload():
    searchIndex.load(get_newest_index_path(index_dir))
    return Response(status=201)


@app.route("/admin/index/<prefix>", methods=["POST"])
def update(prefix):
    """
    Content-type : application/json
    Body:
        { "words" : list of words to update }
    """
    prefix = decompose_korean(prefix)
    word_list = request.json["words"][:searchIndex.max_heap_size]
    searchIndex.update(prefix, word_list)

    increment_path = os.path.join(index_dir, searchIndex.version.split(".")[0])
    increment_path = os.path.join(increment_path, "increment.bin")
    with open(increment_path, "ab") as f:
        write_binary_index_element(f, prefix, searchIndex.index[prefix])

    return Response(status=201)


@app.route("/admin/index/<prefix>", methods=["DELETE"])
def delete(prefix):
    """
    Content-type : application/json
    Body:
        { "words" : list of words to update }
    """
    prefix = decompose_korean(prefix)
    searchIndex.delete(prefix, request.json["words"])

    increment_path = os.path.join(index_dir, searchIndex.version.split(".")[0])
    increment_path = os.path.join(increment_path, "increment.bin")
    with open(increment_path, "ab") as f:
        write_binary_index_element(f, prefix, searchIndex.index[prefix])

    return Response(status=200)
