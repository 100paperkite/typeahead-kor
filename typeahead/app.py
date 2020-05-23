import os
import struct
from flask import request
from typeahead import app
from typeahead.index import SearchIndex

max_heap_size = app.config.get("MAX_HEAP_SIZE")
max_prefix_size = app.config.get("MAX_PREFIX_SIZE")
version = app.config.get("DEFAULT_VERSION")
data_dir = app.config.get("INDEX_DIR")

searchIndex = SearchIndex(max_heap_size, max_prefix_size)


@app.before_first_request
def load_index():
    searchIndex.load(data_dir, version)


@app.route("/")
def info():
    return searchIndex.info()


@app.route("/search/<prefix>")
def autocomplete(prefix):
    return str(searchIndex.search(prefix))


@app.route("/healthcheck")
def healthcheck():
    return "healthy"


@app.route("/admin/index/reload", methods=["POST"])
def reload_index():
    pass


@app.route("/admin/index/<prefix>", methods=["POST", "DELETE"])
def update_index(prefix):
    """
    Content-type : application/json
    Body:
        { prefix : list of words to update }
    """
    content = request.json
    update_words = content[prefix]
    # update
    if request.method == "POST":
        if update_words:
            # 0 count indicates manual appending
            searchIndex.index[prefix] = searchIndex.index[prefix][:max_heap_size - len(update_words)]
            searchIndex.index[prefix] = [(0, word) for word in update_words[:max_heap_size]] + searchIndex.index[prefix]
        else:
            searchIndex.index[prefix] = []  # remove all

    # delete certain words from index
    else:
        searchIndex.index[prefix] = [item for item in searchIndex.index[prefix] if item[1] not in update_words]

    # file write
    with open(os.path.join(data_dir, "update.bin"), "ab") as f:
        f.write(struct.pack(f"<B{len(prefix)}s", len(prefix), prefix.encode()))
        for i, (count, word) in enumerate(searchIndex.index[prefix]):
            f.write(struct.pack(f"<B{len(word)}sI", len(word), word.encode(), count))
        if i+1 != max_heap_size:
            f.write(b"\0")
